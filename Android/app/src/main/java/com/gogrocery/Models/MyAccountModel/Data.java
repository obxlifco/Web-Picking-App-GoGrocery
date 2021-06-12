package com.gogrocery.Models.MyAccountModel;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;


public class Data {

    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("user_id")
    @Expose
    private List<UserId> userId = null;
    @SerializedName("password")
    @Expose
    private String password;
    @SerializedName("last_login")
    @Expose
    private Object lastLogin;
    @SerializedName("is_superuser")
    @Expose
    private Boolean isSuperuser;
    @SerializedName("username")
    @Expose
    private String username;
    @SerializedName("first_name")
    @Expose
    private String firstName;
    @SerializedName("last_name")
    @Expose
    private String lastName;
    @SerializedName("email")
    @Expose
    private String email;
    @SerializedName("is_staff")
    @Expose
    private Boolean isStaff;
    @SerializedName("is_active")
    @Expose
    private Boolean isActive;
    @SerializedName("date_joined")
    @Expose
    private String dateJoined;
    @SerializedName("company_id")
    @Expose
    private Integer companyId;
    @SerializedName("business_name")
    @Expose
    private Object businessName;
    @SerializedName("boost_url")
    @Expose
    private Object boostUrl;
    @SerializedName("website_url")
    @Expose
    private Object websiteUrl;
    @SerializedName("company_logo")
    @Expose
    private Object companyLogo;
    @SerializedName("employee_name")
    @Expose
    private Object employeeName;
    @SerializedName("designation")
    @Expose
    private Object designation;
    @SerializedName("image_name")
    @Expose
    private Object imageName;
    @SerializedName("reset_password")
    @Expose
    private String resetPassword;
    @SerializedName("city")
    @Expose
    private String city;
    @SerializedName("state")
    @Expose
    private String state;
    @SerializedName("postcode")
    @Expose
    private String postcode;
    @SerializedName("phone")
    @Expose
    private String phone;
    @SerializedName("issuperadmin")
    @Expose
    private String issuperadmin;
    @SerializedName("lead_manager_id")
    @Expose
    private Object leadManagerId;
    @SerializedName("createdby_id")
    @Expose
    private Object createdbyId;
    @SerializedName("created_date")
    @Expose
    private String createdDate;
    @SerializedName("modifiedby_id")
    @Expose
    private Object modifiedbyId;
    @SerializedName("modified_date")
    @Expose
    private String modifiedDate;
    @SerializedName("isblocked")
    @Expose
    private String isblocked;
    @SerializedName("isdeleted")
    @Expose
    private String isdeleted;
    @SerializedName("is_verified")
    @Expose
    private String isVerified;
    @SerializedName("verified_code")
    @Expose
    private Object verifiedCode;
    @SerializedName("refferal_code")
    @Expose
    private Object refferalCode;
    @SerializedName("google_login_id")
    @Expose
    private Object googleLoginId;
    @SerializedName("ip_address")
    @Expose
    private Object ipAddress;
    @SerializedName("device_token_ios")
    @Expose
    private Object deviceTokenIos;
    @SerializedName("device_token_android")
    @Expose
    private Object deviceTokenAndroid;
    @SerializedName("user_type")
    @Expose
    private String userType;
    @SerializedName("access_key")
    @Expose
    private Object accessKey;
    @SerializedName("website_id")
    @Expose
    private Object websiteId;
    @SerializedName("country")
    @Expose
    private Object country;
    @SerializedName("role")
    @Expose
    private Object role;
    @SerializedName("groups")
    @Expose
    private List<Object> groups = null;
    @SerializedName("user_permissions")
    @Expose
    private List<Object> userPermissions = null;

    @SerializedName("gender")
    @Expose
    private String gender;
    @SerializedName("location")
    @Expose
    private String location;


    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public List<UserId> getUserId() {
        return userId;
    }

    public void setUserId(List<UserId> userId) {
        this.userId = userId;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Object getLastLogin() {
        return lastLogin;
    }

    public void setLastLogin(Object lastLogin) {
        this.lastLogin = lastLogin;
    }

    public Boolean getIsSuperuser() {
        return isSuperuser;
    }

    public void setIsSuperuser(Boolean isSuperuser) {
        this.isSuperuser = isSuperuser;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Boolean getIsStaff() {
        return isStaff;
    }

    public void setIsStaff(Boolean isStaff) {
        this.isStaff = isStaff;
    }

    public Boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
    }

    public String getDateJoined() {
        return dateJoined;
    }

    public void setDateJoined(String dateJoined) {
        this.dateJoined = dateJoined;
    }

    public Integer getCompanyId() {
        return companyId;
    }

    public void setCompanyId(Integer companyId) {
        this.companyId = companyId;
    }

    public Object getBusinessName() {
        return businessName;
    }

    public void setBusinessName(Object businessName) {
        this.businessName = businessName;
    }

    public Object getBoostUrl() {
        return boostUrl;
    }

    public void setBoostUrl(Object boostUrl) {
        this.boostUrl = boostUrl;
    }

    public Object getWebsiteUrl() {
        return websiteUrl;
    }

    public void setWebsiteUrl(Object websiteUrl) {
        this.websiteUrl = websiteUrl;
    }

    public Object getCompanyLogo() {
        return companyLogo;
    }

    public void setCompanyLogo(Object companyLogo) {
        this.companyLogo = companyLogo;
    }

    public Object getEmployeeName() {
        return employeeName;
    }

    public void setEmployeeName(Object employeeName) {
        this.employeeName = employeeName;
    }

    public Object getDesignation() {
        return designation;
    }

    public void setDesignation(Object designation) {
        this.designation = designation;
    }

    public Object getImageName() {
        return imageName;
    }

    public void setImageName(Object imageName) {
        this.imageName = imageName;
    }

    public String getResetPassword() {
        return resetPassword;
    }

    public void setResetPassword(String resetPassword) {
        this.resetPassword = resetPassword;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getPostcode() {
        return postcode;
    }

    public void setPostcode(String postcode) {
        this.postcode = postcode;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getIssuperadmin() {
        return issuperadmin;
    }

    public void setIssuperadmin(String issuperadmin) {
        this.issuperadmin = issuperadmin;
    }

    public Object getLeadManagerId() {
        return leadManagerId;
    }

    public void setLeadManagerId(Object leadManagerId) {
        this.leadManagerId = leadManagerId;
    }

    public Object getCreatedbyId() {
        return createdbyId;
    }

    public void setCreatedbyId(Object createdbyId) {
        this.createdbyId = createdbyId;
    }

    public String getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
    }

    public Object getModifiedbyId() {
        return modifiedbyId;
    }

    public void setModifiedbyId(Object modifiedbyId) {
        this.modifiedbyId = modifiedbyId;
    }

    public String getModifiedDate() {
        return modifiedDate;
    }

    public void setModifiedDate(String modifiedDate) {
        this.modifiedDate = modifiedDate;
    }

    public String getIsblocked() {
        return isblocked;
    }

    public void setIsblocked(String isblocked) {
        this.isblocked = isblocked;
    }

    public String getIsdeleted() {
        return isdeleted;
    }

    public void setIsdeleted(String isdeleted) {
        this.isdeleted = isdeleted;
    }

    public String getIsVerified() {
        return isVerified;
    }

    public void setIsVerified(String isVerified) {
        this.isVerified = isVerified;
    }

    public Object getVerifiedCode() {
        return verifiedCode;
    }

    public void setVerifiedCode(Object verifiedCode) {
        this.verifiedCode = verifiedCode;
    }

    public Object getRefferalCode() {
        return refferalCode;
    }

    public void setRefferalCode(Object refferalCode) {
        this.refferalCode = refferalCode;
    }

    public Object getGoogleLoginId() {
        return googleLoginId;
    }

    public void setGoogleLoginId(Object googleLoginId) {
        this.googleLoginId = googleLoginId;
    }

    public Object getIpAddress() {
        return ipAddress;
    }

    public void setIpAddress(Object ipAddress) {
        this.ipAddress = ipAddress;
    }

    public Object getDeviceTokenIos() {
        return deviceTokenIos;
    }

    public void setDeviceTokenIos(Object deviceTokenIos) {
        this.deviceTokenIos = deviceTokenIos;
    }

    public Object getDeviceTokenAndroid() {
        return deviceTokenAndroid;
    }

    public void setDeviceTokenAndroid(Object deviceTokenAndroid) {
        this.deviceTokenAndroid = deviceTokenAndroid;
    }

    public String getUserType() {
        return userType;
    }

    public void setUserType(String userType) {
        this.userType = userType;
    }

    public Object getAccessKey() {
        return accessKey;
    }

    public void setAccessKey(Object accessKey) {
        this.accessKey = accessKey;
    }

    public Object getWebsiteId() {
        return websiteId;
    }

    public void setWebsiteId(Object websiteId) {
        this.websiteId = websiteId;
    }

    public Object getCountry() {
        return country;
    }

    public void setCountry(Object country) {
        this.country = country;
    }

    public Object getRole() {
        return role;
    }

    public void setRole(Object role) {
        this.role = role;
    }

    public List<Object> getGroups() {
        return groups;
    }

    public void setGroups(List<Object> groups) {
        this.groups = groups;
    }

    public List<Object> getUserPermissions() {
        return userPermissions;
    }

    public void setUserPermissions(List<Object> userPermissions) {
        this.userPermissions = userPermissions;
    }


}