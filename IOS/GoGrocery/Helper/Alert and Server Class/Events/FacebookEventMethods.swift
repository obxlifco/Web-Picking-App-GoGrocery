//
//  FacebookEventMethods.swift
//  GoGrocery
//
//  Created by NAV63 on 09/06/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import Foundation
import UIKit
import FacebookCore
//MARK:- View Content
public func logViewContentEvent(contentType: String, contentData: String ,contentId: String ,currency: String ,price: Double) {
    let parameters = [
        AppEvents.ParameterName.contentType.rawValue: contentType,
        AppEvents.ParameterName.content.rawValue: contentData,
        AppEvents.ParameterName.contentID.rawValue: contentId,
        AppEvents.ParameterName.currency.rawValue: currency
    ]
    AppEvents.logEvent(.viewedContent, valueToSum: price, parameters: parameters)
}
//MARK:- Search Content
public func logSearchEvent( content_ID: String ,content_Type: String ,currency: String, valueToSum: String) {
    let parameters = [
        AppEvents.ParameterName("Content_ID").rawValue: content_ID,
        AppEvents.ParameterName("Content_Type").rawValue: content_Type,
        AppEvents.ParameterName("Currency").rawValue: currency,
        AppEvents.ParameterName("ValueToSum").rawValue: valueToSum
    ]

    AppEvents.logEvent(.init("Search"), parameters: parameters)
}
//MARK:- Add To Cart
public func logAddToCartEvent( content_ID: String ,content_Type: String ,currency: String ,valueToSum: String) {
    let parameters = [
        AppEvents.ParameterName("Content_ID").rawValue: content_ID,
        AppEvents.ParameterName("Content_Type").rawValue: content_Type,
        AppEvents.ParameterName("Currency").rawValue: currency,
        AppEvents.ParameterName("ValueToSum").rawValue: valueToSum
    ]
    AppEvents.logEvent(.init("Add to cart"), parameters: parameters)
}
//MARK:- Add To Wishlist
 public func logAdd_to_wishlistEvent(content_ID: String,content_Type: String,currency: String, valueToSum: String) {
    let parameters = [
        AppEvents.ParameterName("Content_ID").rawValue: content_ID,
        AppEvents.ParameterName("Content_Type").rawValue: content_Type,
        AppEvents.ParameterName("Currency").rawValue: currency,
        AppEvents.ParameterName("ValueToSum").rawValue: valueToSum
    ]
    AppEvents.logEvent(.init("Add_to_wishlist"), parameters: parameters)
}
//MARK:- Initiate Checkout
public func logInitiateCheckoutEvent( contentIds: String, contentName: String, contentType: String, numItems: String,value: String, currency: String) {
    let parameters = [
        AppEvents.ParameterName("contentIds").rawValue: contentIds,
        AppEvents.ParameterName("contentName").rawValue: contentName,
        AppEvents.ParameterName("contentType").rawValue: contentType,
        AppEvents.ParameterName("numItems").rawValue: numItems,
        AppEvents.ParameterName("value").rawValue: value,
        AppEvents.ParameterName("currency").rawValue: currency
    ]

    AppEvents.logEvent(.init("Initiate_checkout"), parameters: parameters)
}
//MARK:- Rate Product
public func logRateEvent( content_ID: String,content_Type: String, currency: String, valueToSum: String) {
    let parameters = [
        AppEvents.ParameterName("Content_ID").rawValue: content_ID,
        AppEvents.ParameterName("Content_Type").rawValue: content_Type,
        AppEvents.ParameterName("Currency").rawValue: currency,
        AppEvents.ParameterName("ValueToSum").rawValue: valueToSum
    ]
    AppEvents.logEvent(.init("Rate"), parameters: parameters)
}

//MARK:- View Product

public func logViewProductDetailEvent(contentName: String ,contentCategory: String, contentIds: String, content_type: String , value: String ,currency: String
) {
    let parameters = [
        AppEvents.ParameterName("contentName").rawValue: contentName,
        AppEvents.ParameterName("contentCategory").rawValue: contentCategory,
        AppEvents.ParameterName("contentIds").rawValue: contentIds,
        AppEvents.ParameterName("content_type").rawValue: content_type,
        AppEvents.ParameterName("value").rawValue: value,
        AppEvents.ParameterName("currency").rawValue: currency
    ]

    AppEvents.logEvent(.init("View Product Detail"), parameters: parameters)
}

//MARK:- Add Payment Info
public func logAddPaymentInfoEvent(contentIds: String, contentName: String,contentType: String, numItems: String, value: String, currency: String, contents: [String:Any]) {
    let parameters = [
        AppEvents.ParameterName("contentIds").rawValue: contentIds,
        AppEvents.ParameterName("contentName").rawValue: contentName,
        AppEvents.ParameterName("contentType").rawValue: contentType,
        AppEvents.ParameterName("numItems").rawValue: numItems,
        AppEvents.ParameterName("value").rawValue: value,
        AppEvents.ParameterName("currency").rawValue: currency,
        AppEvents.ParameterName("contents").rawValue: contents
        ] as [String : Any]

    AppEvents.logEvent(.init("AddPaymentInfo"), parameters: parameters)
}

//MARK:- Purchase
public func logPurchaseEvent( contentIds: String,contentName: String,contentType: String,numItems: String, value: String, currency: String,contents: [String:Any]) {
    let parameters = [
        AppEvents.ParameterName("contentIds").rawValue: contentIds,
        AppEvents.ParameterName("contentName").rawValue: contentName,
        AppEvents.ParameterName("contentType").rawValue: contentType,
        AppEvents.ParameterName("numItems").rawValue: numItems,
        AppEvents.ParameterName("value").rawValue: value,
        AppEvents.ParameterName("currency").rawValue: currency,
        AppEvents.ParameterName("contents").rawValue: contents
        ] as [String : Any]

    AppEvents.logEvent(.init("Purchase"), parameters: parameters)
}

