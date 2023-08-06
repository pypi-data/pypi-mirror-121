import pytest
from aviv_aws_costexplorer import costcategory


def test_costcategory():
    cc = costcategory.CostCategory(Name="ByEntity")
    assert isinstance(cc, costcategory.CostCategory)
    assert cc.Name == 'ByEntity'

def test_costcategories():
    r = {"Value": "vo", "Rule": {"CostCategories": {"Key": "CostCenter", "Values": ["a", "cost-centers"]}}}
    cc = costcategory.CostCategories(_cli='boto3cli', __root__=[{"Name": "xo", "Rules": [r]}])
    assert isinstance(cc, costcategory.CostCategories)
    assert cc._cli == 'boto3cli'
    # Ensure cli is passed on to CostCategory
    assert cc._cli == cc.get('xo')._cli

    # cc = costcategory.CostCategories(_cli='boto3cli', stuff=42, __root__=[r])
    xorules = cc.get("xo").Rules
    assert xorules.get("vo") == xorules.find('a')

    assert '_cli' not in cc.get("xo").dict()
