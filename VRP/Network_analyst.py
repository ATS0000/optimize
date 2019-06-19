import arcpy
orders = arcpy.FeatureSet()
orders.load("Stores")
depots = arcpy.FeatureSet()
depots.load("DistributionCenter")
routes = arcpy.RecordSet()
routes.load("RoutesTable")
arcpy.na.SolveVehicleRoutingProblem(orders, depots, routes, "","Minutes",
                                    "Miles", "Streets_ND")
