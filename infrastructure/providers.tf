terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "tfstatexyz"
    container_name       = "tfstate"
    key                  = "default.tfstate"
  }
}

provider "azurerm" {
  features {}
}
