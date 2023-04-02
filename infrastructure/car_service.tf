# resource "azurerm_resource_group" "test-gh" {
#   name     = "rg-test-gh"
#   location = "northeurope"
# }

# resource "azurerm_resource_group" "car_service" {
#   name     = "rg-car-service"
#   location = "northeurope"
# }

# resource "random_string" "rnd_suffix" {
#   length      = 4
#   min_numeric = 4
# }

# resource "azurerm_storage_account" "car_service_storage_acc" {
#   name                     = "carservice${random_string.rnd_suffix}"
#   resource_group_name      = azurerm_resource_group.car_service.name
#   location                 = azurerm_resource_group.car_service.location
#   account_tier             = "Standard"
#   account_replication_type = "RA-GRS"
# }

# resource "azurerm_storage_container" "car_service_container" {
#   name                  = "service"
#   storage_account_name  = azurerm_storage_account.car_service_storage_acc.name
#   container_access_type = "private"
# }

# resource "azurerm_storage_blob" "blob1" {
#   name                   = "my-awesome-content.zip"
#   storage_account_name   = azurerm_storage_account.car_service_storage_acc.name
#   storage_container_name = azurerm_storage_container.car_service_container.name
#   type                   = "Block"
#   source                 = "some-local-file.zip"
# }
