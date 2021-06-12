//
//  AddcCart+CoreDataProperties.swift
//  
//
//  Created by BMS-09-M on 09/01/20.
//
//

import Foundation
import CoreData


extension AddcCart {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<AddcCart> {
        return NSFetchRequest<AddcCart>(entityName: "AddcCart")
    }

    @NSManaged public var quantity: String!
    @NSManaged public var product_id: String!
    @NSManaged public var cost: String!

}
