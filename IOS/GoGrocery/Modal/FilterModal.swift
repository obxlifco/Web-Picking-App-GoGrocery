//
//  FilterModal.swift
//  GoGrocery
//
//  Created by BMS-09-M on 14/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//
/*
import Foundation

// MARK: - FilterModalElement
struct FilterModalElement: Codable {
    let fieldName, fieldID, isVariant, isStatic: String
    let child: [Child]
    let maxPrice: Double?

    enum CodingKeys: String, CodingKey {
        case fieldName = "field_name"
        case fieldID = "field_id"
        case isVariant = "is_variant"
        case isStatic = "is_static"
        case child
        case maxPrice = "max_price"
    }
}

// MARK: - Child
struct Child: Codable {
    let id, parentID: Int?
    let displayOrder: JSONNull?
    let name: String
    let childDescription: JSONNull?
    let image, thumbImage, bannerImage, pageTitle: String?
    let metaDescription, metaKeywords: JSONNull?
    let categoryURL: String?
    let slug: String?
    let type: JSONNull?
    let websiteID: Int?
    let isEbayStoreCategory: String?
    let customerGroupID: JSONNull?
    let displayMobileApp, showNavigation: String?
    let productCount: Int?
    let min: Double?
    let max: Max?

    enum CodingKeys: String, CodingKey {
        case id
        case parentID = "parent_id"
        case displayOrder = "display_order"
        case name
        case childDescription = "description"
        case image
        case thumbImage = "thumb_image"
        case bannerImage = "banner_image"
        case pageTitle = "page_title"
        case metaDescription = "meta_description"
        case metaKeywords = "meta_keywords"
        case categoryURL = "category_url"
        case slug, type
        case websiteID = "website_id"
        case isEbayStoreCategory = "is_ebay_store_category"
        case customerGroupID = "customer_group_id"
        case displayMobileApp = "display_mobile_app"
        case showNavigation = "show_navigation"
        case productCount = "product_count"
        case min, max
    }
}

enum Max: Codable {
    case integer(Int)
    case string(String)

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if let x = try? container.decode(Int.self) {
            self = .integer(x)
            return
        }
        if let x = try? container.decode(String.self) {
            self = .string(x)
            return
        }
        throw DecodingError.typeMismatch(Max.self, DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Wrong type for Max"))
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch self {
        case .integer(let x):
            try container.encode(x)
        case .string(let x):
            try container.encode(x)
        }
    }
}

typealias FilterModal = [FilterModalElement]

// MARK: - Encode/decode helpers

class JSONNull: Codable, Hashable {

    public static func == (lhs: JSONNull, rhs: JSONNull) -> Bool {
        return true
    }

    public var hashValue: Int {
        return 0
    }

    public init() {}

    public required init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if !container.decodeNil() {
            throw DecodingError.typeMismatch(JSONNull.self, DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Wrong type for JSONNull"))
        }
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encodeNil()
    }
}
 */
