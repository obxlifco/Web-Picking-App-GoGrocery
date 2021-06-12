// This file was generated from JSON Schema using quicktype, do not modify it directly.
// To parse the JSON, add this file to your project and do:
//
//   let menuList = try? newJSONDecoder().decode(MenuList.self, from: jsonData)

import Foundation

// MARK: - MenuList
struct MenuList: Codable {
    var status: Int?
    var menuBar: [MenuBar]?
    var cmsMenu: [CMSMenu]?

    enum CodingKeys: String, CodingKey {
        case status
        case menuBar = "menu_bar"
        case cmsMenu = "cms_menu"
    }
}

// MARK: - CMSMenu
struct CMSMenu: Codable {
    var id, parentID, pageID: Int?
    var pageDetails: [PageDetail]?
    var child: [CMSMenu]?
    var grandParentID: Int?

    enum CodingKeys: String, CodingKey {
        case id
        case parentID = "parent_id"
        case pageID = "page_id"
        case pageDetails = "page_details"
        case child
        case grandParentID = "grand_parent_id"
    }
}

// MARK: - PageDetail
struct PageDetail: Codable {
    var id: Int?
    var pageName, pageTitle, url, metaKey: String?
    var metaData, metaDesc: String?

    enum CodingKeys: String, CodingKey {
        case id
        case pageName = "page_name"
        case pageTitle = "page_title"
        case url
        case metaKey = "meta_key"
        case metaData = "meta_data"
        case metaDesc = "meta_desc"
    }
}

// MARK: - MenuBar
struct MenuBar: Codable {
    var id, parentID: Int?
    var displayOrder: Int?
    var name: String?
    var menuBarDescription: String?
    var image: String?
    var thumbImage: ThumbImage?
    var bannerImage: BannerImage?
    var pageTitle: String?
    var metaDescription, metaKeywords: String?
    var categoryURL: String?
    var slug: String?
    var type: JSONNull?
    var websiteID: Int?
    var isEbayStoreCategory: DisplayMobileApp?
    var customerGroupID: JSONNull?
    var displayMobileApp, showNavigation: DisplayMobileApp?
    var productCount: Int?
    var langData: [JSONAny]?
    var child: [Child]?
    var grandParentID: Int?

    enum CodingKeys: String, CodingKey {
        case id
        case parentID = "parent_id"
        case displayOrder = "display_order"
        case name
        case menuBarDescription = "description"
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
        case langData = "lang_data"
        case child
        case grandParentID = "grand_parent_id"
    }
}
// MARK: - Child
struct Child: Codable {
    let id, parentID: Int?
  //  let displayOrder: AnyType?
    let name: String?
    let childDescription: String?
    let image: String?
    let thumbImage: String?
    let bannerImage: String?
    let pageTitle: String?
    let metaDescription, metaKeywords: String?
    let categoryURL: String?
    let slug: String?
   // let type: AnyType?
    let websiteID: Int?
    let isEbayStoreCategory: String?
 //   let customerGroupID: AnyType?
    let displayMobileApp, showNavigation: String?
    let grandParentID: Int?
    let child: [Child]?

    enum CodingKeys: String, CodingKey {
        case id
        case parentID = "parent_id"
     //   case displayOrder = "display_order"
        case name
        case childDescription = "description"
        case image
        case thumbImage = "thumb_image"
        case bannerImage = "banner_image"
        case pageTitle = "page_title"
        case metaDescription = "meta_description"
        case metaKeywords = "meta_keywords"
        case categoryURL = "category_url"
        case slug
        case websiteID = "website_id"
        case isEbayStoreCategory = "is_ebay_store_category"
     //   case customerGroupID = "customer_group_id"
        case displayMobileApp = "display_mobile_app"
        case showNavigation = "show_navigation"
        case grandParentID = "grand_parent_id"
        case child
    }
}
enum BannerImage: String, Codable {
    case bannerImageBabyJPEG = "bannerImage_baby.jpeg"
    case empty = ""
}

enum DisplayMobileApp: String, Codable {
    case n = "N"
    case y = "Y"
}

enum ThumbImage: String, Codable {
    case empty = ""
    case iconImageBabyPNG = "IconImage_baby.png"
    case iconImageBakeryPNG = "IconImage_bakery.png"
    case iconImageBeveragesJuicesPNG = "IconImage_beverages--juices.png"
    case iconImageChilledFrozenPNG = "IconImage_chilled--frozen.png"
    case iconImageEtisalatPNG = "IconImage_etisalat.png"
    case iconImageFruitsVegetablesPNG = "IconImage_fruits--vegetables.png"
}

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

class JSONCodingKey: CodingKey {
    let key: String

    required init?(intValue: Int) {
        return nil
    }

    required init?(stringValue: String) {
        key = stringValue
    }

    var intValue: Int? {
        return nil
    }

    var stringValue: String {
        return key
    }
}

class JSONAny: Codable {

    let value: Any

    static func decodingError(forCodingPath codingPath: [CodingKey]) -> DecodingError {
        let context = DecodingError.Context(codingPath: codingPath, debugDescription: "Cannot decode JSONAny")
        return DecodingError.typeMismatch(JSONAny.self, context)
    }

    static func encodingError(forValue value: Any, codingPath: [CodingKey]) -> EncodingError {
        let context = EncodingError.Context(codingPath: codingPath, debugDescription: "Cannot encode JSONAny")
        return EncodingError.invalidValue(value, context)
    }

    static func decode(from container: SingleValueDecodingContainer) throws -> Any {
        if let value = try? container.decode(Bool.self) {
            return value
        }
        if let value = try? container.decode(Int64.self) {
            return value
        }
        if let value = try? container.decode(Double.self) {
            return value
        }
        if let value = try? container.decode(String.self) {
            return value
        }
        if container.decodeNil() {
            return JSONNull()
        }
        throw decodingError(forCodingPath: container.codingPath)
    }

    static func decode(from container: inout UnkeyedDecodingContainer) throws -> Any {
        if let value = try? container.decode(Bool.self) {
            return value
        }
        if let value = try? container.decode(Int64.self) {
            return value
        }
        if let value = try? container.decode(Double.self) {
            return value
        }
        if let value = try? container.decode(String.self) {
            return value
        }
        if let value = try? container.decodeNil() {
            if value {
                return JSONNull()
            }
        }
        if var container = try? container.nestedUnkeyedContainer() {
            return try decodeArray(from: &container)
        }
        if var container = try? container.nestedContainer(keyedBy: JSONCodingKey.self) {
            return try decodeDictionary(from: &container)
        }
        throw decodingError(forCodingPath: container.codingPath)
    }

    static func decode(from container: inout KeyedDecodingContainer<JSONCodingKey>, forKey key: JSONCodingKey) throws -> Any {
        if let value = try? container.decode(Bool.self, forKey: key) {
            return value
        }
        if let value = try? container.decode(Int64.self, forKey: key) {
            return value
        }
        if let value = try? container.decode(Double.self, forKey: key) {
            return value
        }
        if let value = try? container.decode(String.self, forKey: key) {
            return value
        }
        if let value = try? container.decodeNil(forKey: key) {
            if value {
                return JSONNull()
            }
        }
        if var container = try? container.nestedUnkeyedContainer(forKey: key) {
            return try decodeArray(from: &container)
        }
        if var container = try? container.nestedContainer(keyedBy: JSONCodingKey.self, forKey: key) {
            return try decodeDictionary(from: &container)
        }
        throw decodingError(forCodingPath: container.codingPath)
    }

    static func decodeArray(from container: inout UnkeyedDecodingContainer) throws -> [Any] {
        var arr: [Any] = []
        while !container.isAtEnd {
            let value = try decode(from: &container)
            arr.append(value)
        }
        return arr
    }

    static func decodeDictionary(from container: inout KeyedDecodingContainer<JSONCodingKey>) throws -> [String: Any] {
        var dict = [String: Any]()
        for key in container.allKeys {
            let value = try decode(from: &container, forKey: key)
            dict[key.stringValue] = value
        }
        return dict
    }

    static func encode(to container: inout UnkeyedEncodingContainer, array: [Any]) throws {
        for value in array {
            if let value = value as? Bool {
                try container.encode(value)
            } else if let value = value as? Int64 {
                try container.encode(value)
            } else if let value = value as? Double {
                try container.encode(value)
            } else if let value = value as? String {
                try container.encode(value)
            } else if value is JSONNull {
                try container.encodeNil()
            } else if let value = value as? [Any] {
                var container = container.nestedUnkeyedContainer()
                try encode(to: &container, array: value)
            } else if let value = value as? [String: Any] {
                var container = container.nestedContainer(keyedBy: JSONCodingKey.self)
                try encode(to: &container, dictionary: value)
            } else {
                throw encodingError(forValue: value, codingPath: container.codingPath)
            }
        }
    }

    static func encode(to container: inout KeyedEncodingContainer<JSONCodingKey>, dictionary: [String: Any]) throws {
        for (key, value) in dictionary {
            let key = JSONCodingKey(stringValue: key)!
            if let value = value as? Bool {
                try container.encode(value, forKey: key)
            } else if let value = value as? Int64 {
                try container.encode(value, forKey: key)
            } else if let value = value as? Double {
                try container.encode(value, forKey: key)
            } else if let value = value as? String {
                try container.encode(value, forKey: key)
            } else if value is JSONNull {
                try container.encodeNil(forKey: key)
            } else if let value = value as? [Any] {
                var container = container.nestedUnkeyedContainer(forKey: key)
                try encode(to: &container, array: value)
            } else if let value = value as? [String: Any] {
                var container = container.nestedContainer(keyedBy: JSONCodingKey.self, forKey: key)
                try encode(to: &container, dictionary: value)
            } else {
                throw encodingError(forValue: value, codingPath: container.codingPath)
            }
        }
    }

    static func encode(to container: inout SingleValueEncodingContainer, value: Any) throws {
        if let value = value as? Bool {
            try container.encode(value)
        } else if let value = value as? Int64 {
            try container.encode(value)
        } else if let value = value as? Double {
            try container.encode(value)
        } else if let value = value as? String {
            try container.encode(value)
        } else if value is JSONNull {
            try container.encodeNil()
        } else {
            throw encodingError(forValue: value, codingPath: container.codingPath)
        }
    }

    public required init(from decoder: Decoder) throws {
        if var arrayContainer = try? decoder.unkeyedContainer() {
            self.value = try JSONAny.decodeArray(from: &arrayContainer)
        } else if var container = try? decoder.container(keyedBy: JSONCodingKey.self) {
            self.value = try JSONAny.decodeDictionary(from: &container)
        } else {
            let container = try decoder.singleValueContainer()
            self.value = try JSONAny.decode(from: container)
        }
    }

    public func encode(to encoder: Encoder) throws {
        if let arr = self.value as? [Any] {
            var container = encoder.unkeyedContainer()
            try JSONAny.encode(to: &container, array: arr)
        } else if let dict = self.value as? [String: Any] {
            var container = encoder.container(keyedBy: JSONCodingKey.self)
            try JSONAny.encode(to: &container, dictionary: dict)
        } else {
            var container = encoder.singleValueContainer()
            try JSONAny.encode(to: &container, value: self.value)
        }
    }
}
