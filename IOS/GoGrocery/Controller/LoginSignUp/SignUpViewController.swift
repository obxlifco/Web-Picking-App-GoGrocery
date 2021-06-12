//
//  SignUpViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 19/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//

import UIKit
import CountryPickerView
import SwiftyJSON
import GoogleSignIn
import Alamofire
import AuthenticationServices
//import FacebookCore
//import FacebookLogin

class SignUpViewController: UIViewController ,CountryPickerViewDelegate, CountryPickerViewDataSource, GIDSignInDelegate,GIDSignInUIDelegate ,ASAuthorizationControllerDelegate{
    @IBOutlet weak var txtName: UITextField!
    @IBOutlet weak var lblPlaceHolder: UILabel!
    @IBOutlet weak var txtMobile: UITextField!
    @IBOutlet weak var lblMobile: UILabel!
    @IBOutlet weak var txtEmail: UITextField!
    @IBOutlet weak var lblPassword: UILabel!
    @IBOutlet weak var lblEmail: UILabel!
    @IBOutlet weak var txtPassword: UITextField!
    @IBOutlet weak var btnSignUp: UIButton!
    @IBOutlet weak var btnFb: UIButton!
    @IBOutlet weak var btnGoogle: UIButton!
    @IBOutlet weak var countryPickerView: CountryPickerView!
    @IBOutlet weak var lblCountryCode: UILabel!
    @IBOutlet weak var buttonCC: UIButton!
    @IBOutlet weak var lblCC: UILabel!
    @IBOutlet weak var mobileCCTable: UITableView!
    @IBOutlet weak var ccTableView: UIView!
    @IBOutlet weak var ccBackgroundView: UIView!
    @IBOutlet weak var btnHideShowPassword: UIButton!
    @IBOutlet weak var btnBack: UIButton!
    @IBOutlet weak var viewApple: UIView!
    
    var c_code = String()
    var email = String()
    var google_login_id = String()
    var facebook_id = String()
    var apple_login_id = String()
    var user_email = String()
    var first_name = String()
    var last_name = String()
    var phone = String()
    var image_name = String()
    var fbToken = String()
    var ccCode = ["50","52","53","54","55","56","58"]
    var isPassShow = false
    
    func countryPickerView(_ countryPickerView: CountryPickerView, didSelectCountry country: Country) {
        print(country)
        c_code = country.phoneCode
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        
        mobileCCTable.addShadow1()
        btnBack.layer.cornerRadius = btnBack.frame.height/2
        btnBack.addShadow1()
        self.navigationController?.isNavigationBarHidden = true
        allInActive()
        
        btnFb.layer.borderColor = UIColor.lightGray.cgColor
        btnFb.layer.borderWidth = 1
        btnFb.layer.cornerRadius = 5
        
        btnGoogle.layer.borderColor = UIColor.lightGray.cgColor
        btnGoogle.layer.borderWidth = 1
        btnGoogle.layer.cornerRadius = 5
        
        txtName.delegate = self
        txtMobile.delegate = self
        txtEmail.delegate = self
        txtPassword.delegate = self
        
        txtName.layer.cornerRadius = 5
        txtMobile.layer.cornerRadius = 5
        txtEmail.layer.cornerRadius = 5
        txtPassword.layer.cornerRadius = 5
        
        txtEmail.setLeftPaddingPoints(10)
        txtName.setLeftPaddingPoints(10)
        txtMobile.setLeftPaddingPoints(10)
        txtPassword.setLeftPaddingPoints(10)
        
        countryPickerView.delegate = self
        countryPickerView.dataSource = self
        countryPickerView.showPhoneCodeInView = true
        countryPickerView.showCountryCodeInView = false
        countryPickerView.setCountryByCode("IN")
        c_code = "+91"
        
        ccBackgroundView.alpha = 0
        ccTableView.alpha = 0
        lblCountryCode.layer.cornerRadius = 5
        lblCountryCode.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        lblCountryCode.layer.borderWidth = 2
        buttonCC.titleEdgeInsets.left = 10
        buttonCC.layer.cornerRadius = 5
        let tap = UITapGestureRecognizer(target: self, action: #selector(self.handleTap(_:)))
        ccBackgroundView.addGestureRecognizer(tap)
        btnSignUp.layer.cornerRadius = 5
        btnSignUp.addShadow2()
        setUpSignInAppleButton()
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
//    MARK:- APPLE SIGN IN
    func setUpSignInAppleButton() {
        if #available(iOS 13.0, *) {
            let authorizationButton = ASAuthorizationAppleIDButton()
            authorizationButton.addTarget(self, action: #selector(handleAppleIdRequest), for: .touchUpInside)
             self.viewApple.addSubview(authorizationButton)
            
            authorizationButton.translatesAutoresizingMaskIntoConstraints = false
                NSLayoutConstraint.activate([
                  authorizationButton.leadingAnchor.constraint(equalTo: self.viewApple.leadingAnchor, constant: 0),
                  authorizationButton.trailingAnchor.constraint(equalTo: self.viewApple.trailingAnchor, constant: 0),
                  authorizationButton.bottomAnchor.constraint(equalTo: self.viewApple.bottomAnchor, constant: 0),
                    authorizationButton.heightAnchor.constraint(equalToConstant: 50)
                    ])
            //authorizationButton.cornerRadius = 10
            //  print(self.viewLogin.frame)
             // authorizationButton.frame  = CGRect(x: 0, y: 0, width:200 , height: 0)

        }
        else {
            // Fallback on earlier versions
        }
     // self.viewLogin.addArrangedSubview(authorizationButton)

    }
    
    @objc func handleAppleIdRequest() {
        if #available(iOS 13.0, *) {
            let appleIDProvider = ASAuthorizationAppleIDProvider()
            let request = appleIDProvider.createRequest()
            request.requestedScopes = [.fullName, .email]
            let authorizationController = ASAuthorizationController(authorizationRequests: [request])
            authorizationController.delegate = self
            authorizationController.performRequests()
        } else {
            // Fallback on earlier versions
        }
    }
    
    @available(iOS 13.0, *)
    func authorizationController(controller: ASAuthorizationController, didCompleteWithAuthorization authorization: ASAuthorization) {
    if let appleIDCredential = authorization.credential as?  ASAuthorizationAppleIDCredential {
    let userIdentifier = appleIDCredential.user
       
        let fullName = appleIDCredential.fullName
        let firstName = appleIDCredential.fullName?.givenName
        let lastName = appleIDCredential.fullName?.familyName
        let email = appleIDCredential.email
        print("User id is \(userIdentifier) \n Full Name is \(String(describing: fullName)) \n Email id is \(String(describing: email))")
        self.apple_login_id = userIdentifier
        self.first_name = "\(firstName ?? "")"
        self.last_name = "\(lastName ?? "")"
        self.email =  "\(email ?? "")"
        let appleIDProvider = ASAuthorizationAppleIDProvider()
        self.ApiCallToApplesocial()
        appleIDProvider.getCredentialState(forUserID: userIdentifier) {  (credentialState, error) in
             switch credentialState {
                case .authorized:
                    // The Apple ID credential is valid.
                    print("Authorised ------------>>>>>>>>>>>>")
                    break
                case .revoked:
                     print("Revoked ------------>>>>>>>>>>>>")
                    // The Apple ID credential is revoked.
                    break
             case .notFound:
                  print("Not Found ------------>>>>>>>>>>>>")
                break
                    // No credential was found, so show the sign-in UI.
                default:
                    break
             }
        }
    }
    }
    
    @available(iOS 13.0, *)
    func authorizationController(controller: ASAuthorizationController, didCompleteWithError error: Error) {
         print(error.localizedDescription)
     // Handle error.
     }
// MARK:- APPLE SIGN IN ENDS HERE
    
    @IBAction func ccButtontapped(_ sender: Any) {
        ccActive()
        ccBackgroundView.alpha = 1
        ccTableView.alpha = 1
    }
    @objc func handleTap(_ sender: UITapGestureRecognizer? = nil) {
        print("handletap")
        ccInActive()
        UIView.animate(withDuration: 0.3, delay: 0.0, options: [], animations: {
            self.ccBackgroundView.alpha = 0
            self.ccTableView.alpha = 0
           
        })
    }
    @IBAction func btnHideShowPasswordAction(_ sender: Any) {
                if isPassShow == false {
                    txtPassword.isSecureTextEntry = false
                    isPassShow = true
                    btnHideShowPassword.setImage(UIImage(named: "showPassword"), for: .normal)
                } else {
                    txtPassword.isSecureTextEntry = true
                    isPassShow = false
                      btnHideShowPassword.setImage(UIImage(named: "hidePassword"), for: .normal)
                }
    }
    
    
    @IBAction func btnGoogleSignInAction(_ sender: Any) {

          GIDSignIn.sharedInstance()?.uiDelegate = self
          GIDSignIn.sharedInstance()?.delegate = self
           GIDSignIn.sharedInstance().signIn()
      }
    
    // MARK:- Google SignIn
    
    func sign(_ signIn: GIDSignIn!, didSignInFor user: GIDGoogleUser!, withError error: Error!) {
        if user != nil{
            print(user.profile.email)
            self.email = user.profile.email
            self.google_login_id = user.userID
            self.first_name = user.profile.name
            self.email = user.profile.email
            self.image_name = "\(user.profile.imageURL(withDimension: 400)!)"
            ApiCallTosocial()
        }
        else {
            print(error.localizedDescription)
        }
        
    }
    //MARK:- Facebook Delegates
//     func loginManagerDidComplete(_ result: LoginResult) {
//         switch result {
//         case .failed(let error):
//             print(error.localizedDescription)
//             print("FACEBOOK LOGIN FAILED")
//             break
//         case .cancelled:
//             print("FACEBOOK LOGIN CANCELLED")
//             break
//         case .success(let grantedPermissions, let declinedPermissions, let accessToken):
//             print("accessToken----------->>>>>>> \(accessToken.tokenString) ")
//             fbToken = "\(accessToken.tokenString)"
//             getFBUserData()
//             break
//         }
//     }
//    MARK:- Get FB User Data
//    func getFBUserData()
//    {
//        let graphRequest : GraphRequest = GraphRequest(graphPath: "me", parameters: ["fields":"id, email, name, picture.width(480).height(480)"])
//
//        graphRequest.start(completionHandler: { (connection, result, error) -> Void in
//            if ((error) != nil)
//            {
//                print("Error took place: \(error)")
//            }
//            else
//            {
//                print("Print entire fetched result: \(result)")
//                let dict = result as? [String : Any]
//                self.first_name = dict!["name"] as! String
//                 self.facebook_id = "\(dict!["id"] as! String)"
//                let pictureDict = dict!["picture"] as! NSDictionary
//                let dataDict = pictureDict["data"] as! NSDictionary
//                self.image_name = dataDict["url"] as! String
//                self.email = dict!["email"] as! String
//                self.ApiCallTosocial()
//            }
//        })
//    }
    //    MARK:- Active
    func emailtxtActive() {
        self.txtEmail.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtEmail.layer.borderWidth = 2
        self.lblEmail.isHidden = false
    }
    func passwordtxtActive() {
        self.txtPassword.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtPassword.layer.borderWidth = 2
        self.lblPassword.isHidden = false
    }
    func mobiletxtActive() {
        self.txtMobile.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtMobile.layer.borderWidth = 2
        self.lblMobile.isHidden = false
    }
    func nametxtActive() {
        self.txtName.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtName.layer.borderWidth = 2
        self.lblPlaceHolder.isHidden = false
    }
    func ccActive() {
        self.buttonCC.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "CC" {
            self.buttonCC.setTitle("", for: .normal)
        }
        
        self.lblCC.isHidden = false
    }
    //    MARK:- Inactive
    func emailtxtInActive() {
        txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmail.layer.borderWidth = 2
        self.lblEmail.isHidden = true
    }
    func passwordtxtInActive() {
        txtPassword.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmail.layer.borderWidth = 2
        self.lblPassword.isHidden = true
    }
    func nametxtInActive() {
        txtName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtName.layer.borderWidth = 2
        self.lblPlaceHolder.isHidden = true
    }
    func mobileInActive() {
        txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtMobile.layer.borderWidth = 2
        self.lblMobile.isHidden = true
    }
    func ccInActive() {
        buttonCC.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "" {
            self.buttonCC.setTitle("CC", for: .normal)
            self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        }
        
        self.lblCC.isHidden = true
    }
    
        @IBAction func btnBackAction(_ sender: Any) {
        let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
           let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
          self.navigationController?.pushViewController(vc, animated: true)
        }
    
    //    MARK:- All Inactive
    func allInActive() {
        txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmail.layer.borderWidth = 2
        lblEmail.isHidden = true
        
        txtPassword.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtPassword.layer.borderWidth = 2
        lblPassword.isHidden = true
        
        txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtMobile.layer.borderWidth = 2
        lblMobile.isHidden = true
        
        txtName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtName.layer.borderWidth = 2
        lblPlaceHolder.isHidden = true
        
        buttonCC.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "" {
            self.buttonCC.setTitle("CC", for: .normal)
            self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        }
        self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        lblCC.isHidden = true
    }
    
    @IBAction func btnFbAction(_ sender: Any) {
//        let loginManager = LoginManager()
//        loginManager.logIn(permissions: [.publicProfile],viewController: self ) { result in
//            self.loginManagerDidComplete(result)
//            print(result)
//        }
    }
    
    @IBAction func btnsignUpAction(_ sender: Any) {
        if txtEmail.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter email", vc: self)
        }
        else if isValidEmail(testStr: txtEmail.text!) == false {
            createalert(title: "Alert", message: "Please enter valid email id ", vc: self)
        }
        else  if txtPassword.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your paswword", vc: self)
        }
        else  if txtName.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your name", vc: self)
        }else  if txtMobile.text!.trimmingCharacters(in: .whitespaces).count < 7 {
            createalert(title: "Alert", message: "Please enter valid mobile number", vc: self)
        }
        else if buttonCC.currentTitle == "CC" {
            createalert(title: "Alert", message: "Please enter your mobile CC", vc: self)
        }
        else {
            ApiCallToSignUp()
        }
        
    }
    
    @IBAction func btnSignInAction(_ sender: Any) {
        let mainStoryBoard = UIStoryboard(name: "Main", bundle: nil)
        let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
        self.navigationController?.pushViewController(redViewController, animated: true)
    }
    func ApiCallToSignUp() {
        let mobileNo = "971\(buttonCC.currentTitle!)\(txtMobile.text!)"
        var params = [String:Any]()
        params["user_email"] = txtEmail.text!
        params["user_password"] = txtPassword.text!
        params["name"] = txtName.text!.removeExtraSpaces()
        params["phone"] = mobileNo
        params["address"] = "TEST"
        params["carrier_code"] = Int(buttonCC.currentTitle!.trimmingCharacters(in: .whitespaces)) ?? 00
        print(params)
        postMethodSignup(apiName: "signup/", params: params as NSDictionary , vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                UserDefaults.standard.setValue(true, forKey: "is-login")
                UserDefaults.standard.setValue(data["token"]?.stringValue, forKey: "token")
                UserDefaults.standard.setValue(data["first_name"]?.stringValue, forKey: "first_name")
                UserDefaults.standard.setValue(data["last_name"]?.stringValue, forKey: "last_name")
                UserDefaults.standard.synchronize()
                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                 let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                    vc.userDict = response["data"].dictionaryValue
                   // self.navigationController?.pushViewController(vc, animated: true)
                self.ApiCallToResisterDevice()
            }
            else {
                let message = response["message"].stringValue
                createalert(title: "Alert", message: message, vc: self)
            }
        }
        
    }
    
    //    MARK:- Api Calling
    func ApiCallTosocial(){
        var params = [String:Any]()
        params["google_login_id"] = self.google_login_id
        params["facebook_id"] = self.facebook_id
        params["phone"] = ""
        params["user_email"] = self.email
        params["image_name"] = self.image_name
        params["last_name"] = self.last_name
        params["first_name"] = self.first_name
        print(params)
        postMethodSocialSignIn(apiName: "social-login/", params: params, vc: self) { (response:JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                UserDefaults.standard.setValue(true, forKey: "is-login")
                UserDefaults.standard.setValue(data["token"]?.stringValue, forKey: "token")
                UserDefaults.standard.setValue(data["first_name"]?.stringValue, forKey: "first_name")
                UserDefaults.standard.setValue(data["last_name"]?.stringValue, forKey: "last_name")
                UserDefaults.standard.synchronize()
//                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
//                let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
//                self.navigationController?.pushViewController(vc, animated: true)
                self.ApiCallToResisterDevice()
            }
            else {  
                createalert(title: "Alert", message: response["message"].stringValue, vc: self)
            }
        }
    }
    
    func ApiCallToApplesocial(){
      //  http://localhost:8086/api/front/v1/apple-login/
        var params = [String:Any]()
        params["apple_login"] = self.apple_login_id
        params["user_email"] = self.email
        params["first_name"] = self.first_name
        params["last_name"] = self.last_name
        print(params)
        postMethodSocialSignInApple(apiName: "apple-login/", params: params, vc: self) { (response:JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                UserDefaults.standard.setValue(true, forKey: "is-login")
                UserDefaults.standard.setValue(data["token"]?.stringValue, forKey: "token")
                UserDefaults.standard.setValue(data["first_name"]?.stringValue, forKey: "first_name")
                UserDefaults.standard.setValue(data["last_name"]?.stringValue, forKey: "last_name")
                UserDefaults.standard.synchronize()
//                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
//                let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
              //  self.navigationController?.pushViewController(vc, animated: true)
                self.ApiCallToResisterDevice()
            }
            else {
                createalert(title: "Alert", message: response["message"].stringValue, vc: self)
            }
        }
    }
    
    func ApiCallToResisterDevice() {
        let fcmToken = UserDefaults.standard.value(forKey: "fcm_token") as? String ?? ""
        let systemVersion = UIDevice.current.systemVersion
        let appVersion = getAppInfo()
        //deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
      //  params["device_id"] = deviceId
        params["device_token"] = fcmToken
        params["version"] = appVersion
        params["os_version"] = "\(systemVersion)"
        params["device_type"] = "i"
         print(params)
        postMethodRegisterDevice(apiName: "update-device-details/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                    let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                     self.navigationController?.pushViewController(vc, animated: true)
            }
            else {
                let message = response["message"].stringValue
                createalert(title: "Alert", message: message, vc: self)
            }
        }
    }
    
    func getAppInfo()->String {
        let dictionary = Bundle.main.infoDictionary!
        let version = dictionary["CFBundleShortVersionString"] as! String
        let build = dictionary["CFBundleVersion"] as! String
        return build
    }
}


extension SignUpViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == txtEmail {
            emailtxtActive()
            passwordtxtInActive()
            mobileInActive()
            nametxtInActive()
        }
        else  if textField == txtPassword {
            passwordtxtActive()
            emailtxtInActive()
            mobileInActive()
            nametxtInActive()
        }
        else if textField == txtMobile {
            mobiletxtActive()
            emailtxtInActive()
            passwordtxtInActive()
            nametxtInActive()
        }
        else {
            nametxtActive()
            passwordtxtInActive()
            emailtxtInActive()
            mobileInActive()
        }
    }
    func textFieldDidEndEditing(_ textField: UITextField, reason: UITextField.DidEndEditingReason) {
        if textField == txtEmail {
            emailtxtInActive()
            passwordtxtInActive()
        }
        else {
            emailtxtInActive()
            passwordtxtInActive()
        }
    }
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
        
        if(textField == txtEmail)  {
            if string == " " {
                if range.location == 0 {
                    return false
                }
                  return false
            }

            return true
        }
        else if(textField == txtPassword)  {
            if string == " " {
                if range.location == 0 {
                    return false
                }
                  return false
            }

            return true
        }
        
        
        if textField == txtMobile {
            guard let text = textField.text else { return true }
            let newLength = text.count + string.count - range.length
            return newLength <= 7
        }
        
        return true
    }
}

// MARK:- CCTable data source and Delegate
extension SignUpViewController : UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return ccCode.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = mobileCCTable.dequeueReusableCell(withIdentifier: "MobileCCTableViewCell") as! MobileCCTableViewCell
        cell.ccLabel.text = ccCode[indexPath.row]
        cell.selectionStyle = .none
        return cell
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.buttonCC.setTitle(ccCode[indexPath.row], for: .normal)
        self.buttonCC.setTitleColor(.black, for: .normal)
        ccInActive()
        ccBackgroundView.alpha = 0
        ccTableView.alpha = 0
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 60
    }
    
}
extension String {

    func removeExtraSpaces() -> String {
        var data  = ""
        var numberOfSpace = 0
        let items = self.components(separatedBy: .whitespaces).filter{!$0.isEmpty}
        for item in items{
            if item == " "{
                numberOfSpace = numberOfSpace + 1
            }else{
                numberOfSpace = 0
            }
            if numberOfSpace == 1 || numberOfSpace == 0 {
                data =  data + item
                //data.append(item)
            }
        }
        return data
    }
}

