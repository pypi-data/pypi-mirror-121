import logging
import typing
import pydantic
import boto3
from . import base

class CostCategoryRuleDefinition(pydantic.BaseModel):
    """
    type: typing.Literal["Dimensions", "Tags", "CostCategories"]="Dimensions"

    # For type == 'Dimensions':
    Key: typing.Literal["LINKED_ACCOUNT", "INSTANCE_TYPE", "REGION", "SERVICE"]="LINKED_ACCOUNT"
    """
    type: str="Dimensions"
    Key: str="LINKED_ACCOUNT"
    Values: typing.List[str]
    MatchOptions: typing.List[typing.Literal["EQUALS", "ABSENT", "STARTS_WITH", "ENDS_WITH", "CONTAINS", "CASE_SENSITIVE", "CASE_INSENSITIVE"]]=["EQUALS"]

    def dict(self, **attr):
        return {self.type: super().dict(**attr)}

class CostCategoryRule(pydantic.BaseModel):
    Value: str
    Rule: CostCategoryRuleDefinition
    Type: typing.Literal["REGULAR", "INHERITED_VALUE"]=None
    InheritedValue: dict=None

class CostCategoryRules(pydantic.BaseModel):
    __root__: typing.List[CostCategoryRule]=[]

    def append(self, value) -> None:
        self.__root__.append(value)
        super().__init__(__root__=self.__root__)

    def __getitem__(self, item: int) -> int:
        return self.__root__[item]

    def __setitem__(self, item: int, value) -> None:
        self.__root__[item] = value
        super().__init__(__root__=self.__root__)

    def names(self) -> list:
        return list(r.Value for r in self.__root__)

    def get(self, name) -> CostCategoryRule:
        return next(filter(lambda r: r.Value == name, self.__root__), None)

    def find(self, value) -> CostCategoryRule:
        for rule in self.__root__:
            if value in rule.Rule.Values:
                return rule
        return None

class CostCategory(pydantic.BaseModel):
    class Config:
        validate_assignment = True

    Name: str
    CostCategoryArn: str=None
    EffectiveStart: str=None
    RuleVersion: str='CostCategoryExpression.v1'
    Rules: CostCategoryRules=CostCategoryRules()
    _cli: boto3.Session.client=boto3.client('ce')

    def __init__(self, **data) -> None:
        if 'Name' in data and 'CostCategoryArn' not in data:
            data['CostCategoryArn'] = self.get_arn(data['Name'])
        super().__init__(**data)
        if self.CostCategoryArn:
            logging.warning(f"> for {self.CostCategoryArn}")
        else:
            logging.warning(f"> new CostCategory {self.Name}")

    def dict(self) -> dict:
        return super().dict(exclude_none=True)

    def sync(self):
        if self.CostCategoryArn:
            return self._cli.update_cost_category_definition(self.dict())
        return self._cli.create_cost_category_definition(self.dict())

    def describe(self):
        definition = self._cli.describe_cost_category_definition(CostCategoryArn=self.CostCategoryArn)['CostCategory']
        for desc in definition['Rules']:
            rk = list(desc['Rule'].keys())[0]
            desc['Rule'] = desc['Rule'][rk]
            desc['Rule']['type'] = rk
        # logging.warning(definition)
        super().__init__(**definition)
    
    def get_arn(self, name):
        definitions = self._cli.list_cost_category_definitions()['CostCategoryReferences']
        cost_category = next(filter(lambda x: x['Name'] == name, definitions), None)
        if not cost_category:
            logging.warning(f"Available CostCategories: {list(c['Name'] for c in definitions)}")
            return None
        return cost_category['CostCategoryArn']

class CostCategories(pydantic.BaseModel):
    __root__: typing.List[CostCategory]=[]
    _cli: boto3.Session.client=boto3.client('ce')

    def __init__(self, role_arn: str=None, **data: __root__) -> None:
        if role_arn:
            self._cli = base.AWSClient.client('ce', role_arn=role_arn)
        super().__init__(**data)

    def list(self):
        cats = self._cli.list_cost_category_definitions()['CostCategoryReferences']
        for c in cats:
            c['_cli'] = self._cli
        super().__init__(__root__=cats, cli=self._cli)

    def get(self, name) -> CostCategory:
        return next(filter(lambda r: r.Name == name, self.__root__), None)


def diff_CostCategoryRules(cc1: CostCategoryRules, cc2: CostCategoryRules):
    diffs = dict(
        added = list(set(cc1.names()) - set(cc2.names())),
        removed = list(set(cc2.names()) - set(cc1.names())),
        changed = {}
    )
    for rule in list(set(cc1.names()) & set(cc2.names())):
        rtype = cc1.get(rule).Rule.type != cc2.get(rule).Rule.type
        rdiff = set(cc1.get(rule).Rule.Values) != set(cc2.get(rule).Rule.Values)
        if rtype or rdiff:
            diffs['changed'][rule] = dict(
                added = list(set(cc1.get(rule).Rule.Values) - set(cc2.get(rule).Rule.Values)),
                removed = list(set(cc2.get(rule).Rule.Values) - set(cc1.get(rule).Rule.Values))
            )
            if rtype:
                diffs['changed'][rule]['type'] = f"{cc2.get(rule).Rule.type} -> {cc1.get(rule).Rule.type}"

    return diffs
