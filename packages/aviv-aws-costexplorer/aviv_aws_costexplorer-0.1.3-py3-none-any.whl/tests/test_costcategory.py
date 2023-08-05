import pytest
from aviv_aws_costexplorer import costcategory


def test_costcategory():
    cc = costcategory.CostCategory(Name="ByEntity", CostCategoryArn='NA')
    assert isinstance(cc, costcategory.CostCategory)
