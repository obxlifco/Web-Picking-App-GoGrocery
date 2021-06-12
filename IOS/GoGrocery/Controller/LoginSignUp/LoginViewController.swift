
import UIKit
import SwiftyJSON
import SkyFloatingLabelTextField
//import Google
import GoogleSignIn
//import FacebookCore
//import FacebookLogin
import FirebaseAnalytics
import Firebase
import FBSDKLoginKit
import AuthenticationServices
class LoginViewController: UIViewController , GIDSignInDelegate , GIDSignInUIDelegate ,ASAuthorizationControllerDelegate {
    @IBOutlet weak var lblPasswordPlaceholder: UILabel!
    @IBOutlet weak var lblEmailPlaceholder: UILabel!
    @IBOutlet weak var loginstackView: UIStackView!
    @IBOutlet weak var btnGoogleSignIn: UIButton!
    @IBOutlet weak var btnFbSignIn: UIButton!
    @IBOutlet weak var btnSignIn: UIButton!
    @IBOutlet weak var txtEmail: UITextField!
    @IBOutlet weak var txtPassword: UITextField!
    @IBOutlet weak var btnPasswordHideShow: UIButton!
    @IBOutlet weak var btnBack: UIButton!
    @IBOutlet weak var viewApple: UIView!
    var textFields: [SkyFloatingLabelTextField] = []
    var google_login_id = String()
    var facebook_id = String()
    var apple_login_id = String()
    var email = String()
    var first_name = String()
    var last_name = String()
    var phone = String()
    var image_name = String()
    var fbToken = String()
    var userFullName = String()
    var isPassShow = false
    var isForSubstitute = false
    var orderIdForSubstitute = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()

        btnBack.layer.cornerRadius = btnBack.frame.height/2
        btnBack.addShadow1()
        btnFbSignIn.addShadow2()
        btnGoogleSignIn.addShadow2()
        self.navigationController?.isNavigationBarHidden = true
        bothInActive()
        btnSignIn.layer.cornerRadius = 5
        btnSignIn.addShadow2()
        btnGoogleSignIn.layer.cornerRadius = 5
        btnFbSignIn.layer.borderColor = UIColor.lightGray.cgColor
        btnFbSignIn.layer.borderWidth = 1
        btnGoogleSignIn.layer.borderColor = UIColor.lightGray.cgColor
        btnGoogleSignIn.layer.borderWidth = 1
        txtEmail.delegate = self
        txtPassword.delegate = self
        txtEmail.layer.cornerRadius = 5
        txtPassword.layer.cornerRadius = 5
        txtEmail.setLeftPaddingPoints(10)
        txtPassword.setLeftPaddingPoints(10)
        setUpSignInAppleButton()
//        self.ApiCallToResisterDevice()
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
//   MARK:- APPLE SIGN IN START
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
//    MARK:- APPLE SIGN IN ENDS HERE
    
    func LogEvents() {
        Analytics.logEvent(AnalyticsEventSelectContent, parameters: [
        AnalyticsParameterItemID: "id-\(title!)",
        AnalyticsParameterItemName: title!,
        AnalyticsParameterContentType: "cont"
        ])
        
    }

    @IBAction func btnGoogleSignInAction(_ sender: Any) {
         GIDSignIn.sharedInstance()?.uiDelegate = self
         GIDSignIn.sharedInstance()?.delegate = self
          GIDSignIn.sharedInstance().signIn()
     }
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
//    func loginManagerDidComplete(_ result: LoginResult) {
//        switch result {
//        case .failed(let error):
//            print(error.localizedDescription)
//            print("FACEBOOK LOGIN FAILED")
//            break
//        case .cancelled:
//            print("FACEBOOK LOGIN CANCELLED")
//            break
//        case .success(let grantedPermissions, let declinedPermissions, let accessToken):
//            print("accessToken----------->>>>>>> \(accessToken.tokenString) ")
//            fbToken = "\(accessToken.tokenString)"
//            getFBUserData()
//            break
//        }
//    }
    
    //    MARK:- View Customisations
    func emailtxtActive() {
        self.txtEmail.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtEmail.layer.borderWidth = 2
        self.lblEmailPlaceholder.isHidden = false
    }
    func passwordtxtActive() {
        self.txtPassword.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtPassword.layer.borderWidth = 2
        self.lblPasswordPlaceholder.isHidden = false
    }
    func emailtxtInActive() {
     //   txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmail.layer.borderColor = UIColor.lightGray.cgColor
        txtEmail.layer.borderWidth = 2
        self.lblEmailPlaceholder.isHidden = true
    }
    func passwordtxtInActive() {
        txtPassword.layer.borderColor = UIColor.lightGray.cgColor
        txtEmail.layer.borderWidth = 2
        self.lblPasswordPlaceholder.isHidden = true
    }
    func bothInActive() {
        txtEmail.layer.borderColor = UIColor.lightGray.cgColor
        txtEmail.layer.borderWidth = 2
        txtPassword.layer.borderColor = UIColor.lightGray.cgColor
        txtPassword.layer.borderWidth = 2
        self.lblEmailPlaceholder.isHidden = true
        self.lblPasswordPlaceholder.isHidden = true
    }
    @IBAction func btnSignInAction(_ sender: Any) {
        if txtEmail.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter email", vc: self)
        }
        else if txtPassword.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter password", vc: self)
        }
        else if isValidEmail(testStr: txtEmail.text!) == false {
            createalert(title: "Alert", message: "Please enter valid email", vc: self)
        }
        else {
            ApiCallToLogin()
        }
        
    }
//    MARK:- Button Actions
    
    @IBAction func btnPasswordHdeShowAction(_ sender: Any) {
        if isPassShow == false {
            txtPassword.isSecureTextEntry = false
            isPassShow = true
            btnPasswordHideShow.setImage(UIImage(named: "showPassword"), for: .normal)
        } else {
            txtPassword.isSecureTextEntry = true
            isPassShow = false
              btnPasswordHideShow.setImage(UIImage(named: "hidePassword"), for: .normal)
        }

    }

    @IBAction func btnForgetPasswordAction(_ sender: Any) {
 
        let storyboard:UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ForgetPasswordViewController") as! ForgetPasswordViewController
            let backButton = UIBarButtonItem()
            backButton.title = ""
            navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
              UINavigationBar.appearance().tintColor = UIColor.black
            self.navigationController?.pushViewController(vc, animated: true)

    }
    @IBAction func btnBackAction(_ sender: Any) {
    let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
       let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
      self.navigationController?.pushViewController(vc, animated: true)
    }

    // MARK:- FACEBOOK BUTTON ACTION
    @IBAction func btnFbSignInAction(_ sender: Any) {
        let loginManager = LoginManager()
            loginManager.logIn(permissions: ["email","public_profile"], from: self) { [weak self] (result, error) in
                guard error == nil else {
                    // Error occurred
                    print(error!.localizedDescription)
                    //self.showOkAlertBox(title: "Error", message: "Something went wrong.")
                    return
                }

                guard let result = result, !result.isCancelled else {
                    print("User cancelled login")
                    return
                }
                self!.getFBUserData()
            }
    }
    
    func getFBUserData()
    {
        let graphRequest : GraphRequest = GraphRequest(graphPath: "me", parameters: ["fields":"id, email, name, picture.width(480).height(480)"])

        graphRequest.start(completionHandler: { (connection, result, error) -> Void in
            if ((error) != nil)
            {
              print("error is there")
            }
            else
            {
                let dict = result as? [String : Any]
                self.first_name = dict?["name"] as? String ?? ""
                self.facebook_id = "\(dict?["id"] as? String ?? "")"
               // if dict!["picture"] as? NSDictionary
                if (dict?["picture"] as? NSDictionary) != nil {
                    let pictureDict = dict!["picture"] as? NSDictionary
                    let dataDict = pictureDict?["data"] as? NSDictionary
                    self.image_name = dataDict?["url"] as? String ?? ""
                }
                else {

                }
                if dict?.isEmpty == false {
                    if dict?["email"] as? String != "" || dict?["email"] as? String != nil || (dict?["email"] as? String)?.isEmpty != true {
                         self.email = dict?["email"] as? String ?? ""
                    }
                    else {
                       // print(dict!["email"] as! String)
                    }
                }
                self.ApiCallTosocial()
            }
        })
    }
    @IBAction func btnSignUpAction(_ sender: Any) {
        let mainStoryBoard = UIStoryboard(name: "Main", bundle: nil)
        let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "SignUpViewController") as! SignUpViewController
        self.navigationController?.pushViewController(redViewController, animated: true)
    }
    func ApiCallToLogin() {
//        var deviceId : String
//        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        let para:[String : Any] = ["user_mail":self.txtEmail.text!,"user_password":self.txtPassword.text!]
        postMethodReturnJsonLogin(apiName: "login/", params: para, vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
               
                let data = response["data"].dictionaryValue
                UserDefaults.standard.setValue(true, forKey: "is-login")
                UserDefaults.standard.setValue(data["token"]?.stringValue, forKey: "token")
                UserDefaults.standard.setValue(data["first_name"]?.stringValue, forKey: "first_name")
                UserDefaults.standard.setValue(data["last_name"]?.stringValue, forKey: "last_name")
                UserDefaults.standard.synchronize()
                NotificationCenter.default.post(name: Notification.Name("MenuUpdate"), object: nil)
                 self.ApiCallToResisterDevice()
               // self.navigationController?.popViewController(animated: true)
            }
            else {
                let message = response["message"].stringValue
                createalert(title: "Alert", message: message, vc: self)
            }
        }
    }

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
                 NotificationCenter.default.post(name: Notification.Name("MenuUpdate"), object: nil)
                self.ApiCallToResisterDevice()
               // self.navigationController?.popViewController(animated: true)
            }
            else {
                let message = response["message"].stringValue
                createalert(title: "Alert", message: message, vc: self)
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
        
//        params["first_name"] = ""
//        params["last_name"] = ""
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
                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                self.ApiCallToResisterDevice()
               // self.navigationController?.pushViewController(vc, animated: true)
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
                    if self.isForSubstitute {
                        let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                        let vc = storyboard.instantiateViewController(withIdentifier: "SubstituteViewController") as! SubstituteViewController
                        vc.orderId = self.orderIdForSubstitute
                         self.navigationController?.pushViewController(vc, animated: true)
                    } else {
                       self.navigationController?.popViewController(animated: true)
                    }
                    
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
extension LoginViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == txtEmail {
            emailtxtActive()
            passwordtxtInActive()
        }
        else {
            passwordtxtActive()
            emailtxtInActive()
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
            //TextField Validation
        func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool  {

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
             return true
        }
}
