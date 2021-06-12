//
//  FirebaseEventsMethods.swift
//  GoGrocery
//
//  Created by NAV63 on 18/09/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import Foundation
import UIKit
import FirebaseAnalytics

public func AddCart(dictParam : [String:Any]) {
    Analytics.logEvent("add_to_cart", parameters: dictParam)
}

public func ViewProduct(dictParam : [String:Any]) {
    Analytics.logEvent("view_product", parameters:  dictParam)
}

public func AddToWishlist(dictParam : [String:Any]) {
     Analytics.logEvent("add_to_wishlist", parameters: dictParam)
 }
public func Checkout(dictParam : [String:Any]) {
    Analytics.logEvent("checkout", parameters: dictParam)
}
public func PlaceOrder(dictParam : [String:Any]) {
    Analytics.logEvent("place_order", parameters: dictParam)
}
public func Payment(dictParam : [String:Any]) {
    Analytics.logEvent("payment", parameters: dictParam)
}





