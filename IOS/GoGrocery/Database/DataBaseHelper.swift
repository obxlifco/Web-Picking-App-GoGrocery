//
//  DataBaseHelper.swift
//  GoGrocery
//
//  Created by BMS-09-M on 09/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import Foundation
import UIKit
import CoreData

class DataBaseHelper {
    static var sharedInstance = DataBaseHelper()
    let context = (UIApplication.shared.delegate as? AppDelegate)?.persistentContainer.viewContext
    
    func save(object : [String : Any]) {
        let addCart = NSEntityDescription.insertNewObject(forEntityName: "AddcCart" , into : context!) as! AddcCart
        addCart.quantity = (object["quantity"] as? String ?? "")
        addCart.cost = (object["cost"] as? String ?? "")
        addCart.product_id = (object["product_id"] as? String ?? "")
       // print(object)
        do {
            try context?.save()
          //  print("Data Saved")
        } catch {
           // print("Data Not Save")
        }
    }
    func getCartData() -> [AddcCart] {
        var cartData = [AddcCart]()
        let fetchRequest = NSFetchRequest<NSManagedObject>(entityName : "AddcCart")
        do {
            cartData = try context?.fetch(fetchRequest) as! [AddcCart]
        } catch {
         //   print("Cannot get Data")
        }
        return cartData
    }
    func editData(object :[String : Any], i: Int){
        print(i)
        let cart = getCartData()
//        context?.delete(cart[i])
//        cart.remove(at: i)
//
//        let cart1 = getCartData()
//        cart[i].quantity.append(contentsOf: object["quantity"] as! String)
//        cart[i].cost.append(contentsOf: object["cost"] as! String)
//        cart[i].product_id.append(contentsOf: object["product_id"] as! String)
//
        print(i)
        cart[i].quantity = (object["quantity"] as? String ?? "")
        cart[i].cost = (object["cost"] as?  String ?? "")
        cart[i].product_id = (object["product_id"] as? String ?? "")
        do {
            try context?.save()
        }
        catch {
            print("Data is Not edited")
        }

    }
    func delete(index : Int) {
        var cart = getCartData()
        context?.delete(cart[index])
        cart.remove(at: index)
        do {
            try context?.save()
        } catch {
            print("cannot delete data")
        }
    }
    
    func deleteAllRecords() {
       // let delegate = UIApplication.shared.delegate as! AppDelegate
      //  let context = delegate.persistentContainer.viewContext

        let deleteFetch = NSFetchRequest<NSFetchRequestResult>(entityName: "AddcCart")
        let deleteRequest = NSBatchDeleteRequest(fetchRequest: deleteFetch)

        do {
            try context!.execute(deleteRequest)
            try context!.save()
        } catch {
            print ("There was an error")
        }
    }
//    func deleteAll(){
////         var cart = getCartData()
////         context?.delete(AddcCart)
////         cart.removeAll()
////         do {
////             try context?.save()
////         } catch {
////             print("cannot delete data")
////         }
//
//        let fetch = NSFetchRequest<NSFetchRequestResult>(entityName: "AddcCart")
//        let request = NSBatchDeleteRequest(fetchRequest: fetch)
//        let result = try! context!.execute(request)
//     }
    
//    func convertToJSONArray(moArray: [NSManagedObject]) -> Any {
//        var jsonArray: [[String: Any]] = []
//        for item in moArray {
//            var dict: [String: Any] = [:]
//            for attribute in item.entity.attributesByName {
//                //check if value is present, then add key to dictionary so as to avoid the nil value crash
//                if let value = item.value(forKey: attribute.key) {
//                    dict[attribute.key] = value
//                }
//            }
//            jsonArray.append(dict)
//        }
//        return jsonArray
//    }
    
}
