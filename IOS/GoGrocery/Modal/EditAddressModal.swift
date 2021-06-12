// This file was generated from JSON Schema using quicktype, do not modify it directly.
// To parse the JSON, add this file to your project and do:
//
//   let appNotificationModal = try? newJSONDecoder().decode(AppNotificationModal.self, from: jsonData)

import Foundation

// MARK: - AppNotificationModal
struct AppNotificationModal: Codable {
    var statusCode: Int?
    var message, response: String?
    var data: DataClass?

    enum CodingKeys: String, CodingKey {
        case statusCode = "status_code"
        case message, response, data
    }
}

// MARK: - DataClass
struct DataClass: Codable {
    var id, name, email, emailVerifiedAt: String?
    var badgeNo, ethnicity, profileImage, badgeColour: String?
    var age, phone, slug, otpCode: String?
    var createdAt, updatedAt, status, gender: String?
    var dataDescription, deviceToken, deviceType, address: String?
    var city, state, zip, role: String?
    var token: String?
    var roles: [Role]?

    enum CodingKeys: String, CodingKey {
        case id, name, email
        case emailVerifiedAt = "email_verified_at"
        case badgeNo = "badge_no"
        case ethnicity
        case profileImage = "profile_image"
        case badgeColour = "badge_colour"
        case age, phone, slug
        case otpCode = "otp_code"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
        case status, gender
        case dataDescription = "description"
        case deviceToken = "device_token"
        case deviceType = "device_type"
        case address, city, state, zip, role, token, roles
    }
}

// MARK: - Role
struct Role: Codable {
    var id, name, guardName, createdAt: String?
    var updatedAt: String?
    var pivot: Pivot?

    enum CodingKeys: String, CodingKey {
        case id, name
        case guardName = "guard_name"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
        case pivot
    }
}

// MARK: - Pivot
struct Pivot: Codable {
    var modelID, roleID, modelType: String?

    enum CodingKeys: String, CodingKey {
        case modelID = "model_id"
        case roleID = "role_id"
        case modelType = "model_type"
    }
}

