
import UIKit
import SwiftyJSON
class ProfileViewController: UIViewController{
    
    @IBOutlet weak var btnCart: UIButton!
    @IBOutlet weak var btnSearch: UIButton!
    @IBOutlet weak var imgImage: UIImageView!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var lblEmail: UILabel!
    @IBOutlet weak var txtMobile: UILabel!
    @IBOutlet weak var btnCartCount: UIButton!
    var cartArray = [JSON]()
    var navigationType:String = ""
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var badgeCount = Int()
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
        let image = UIImage(named: "cart")?.withRenderingMode(.alwaysTemplate)
        self.btnCart.setImage(image, for: .normal)
        self.btnCart.tintColor = UIColor.white

        //self.btnCart.tintColor = .white
        btnCartCount.layer.cornerRadius = btnCartCount.frame.height/2

        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        ApiCallTogetUserDetails()
        ApiCallToViewCart()
       // ApiCallToGetCartCount()
        self.navigationController?.isNavigationBarHidden = true
    }
//    MARK:- Set Icon Color White

    //    MARK:- Button Actions
    
    @IBAction func btnBackAction(_ sender: Any) {
        if navigationType == "present" {
            dismiss(animated: true, completion: nil)
        }
        else {
            self.navigationController?.popViewController(animated: true)
        }
    }
    
    @IBAction func btnSearchAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "SearchViewController") as! SearchViewController
        self.navigationController?.pushViewController(viewController, animated: true)
    }
    
    @IBAction func btnCartAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        self.navigationController?.pushViewController(viewController, animated: true)
    }
    
    @IBAction func btnEditAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "UpdateProfileViewController") as! UpdateProfileViewController
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnMyOrdersAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "MyOrdersViewController") as! MyOrdersViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
    }
    
    @IBAction func btnMyAddressAction(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "SavedAdressListViewController") as! SavedAdressListViewController
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.pushViewController(vc, animated: true)
    }
    @IBAction func btnWalletAction(_ sender: Any) {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "WalletViewController") as! WalletViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
        }
    }
    @IBAction func btnAccountSettingAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "UpdateProfileViewController") as! UpdateProfileViewController
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnSaveListAction(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveListViewController") as! SaveListViewController
        vc.isFromMySaveList = true
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnLogoutAction(_ sender: Any) {
        ApiCallToLogout()
    }
    //MARK:- Api Calling
    func ApiCallToLogout() {
         let api = "http://gogrocery.ae:81/api/picker-logout/"
       // let api = "http://15.185.126.44:8062/api/picker-logout/"
         var params = [String:Any]()
         params["ip_address"] = ""
          let deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
         params["device_id"] = deviceId
         print(params)
         postMethodSubstitute(apiName: api, params: params, vc: self) { (response:JSON) in
             print(response)
            if response["status"].intValue != 0 {
                UserDefaults.standard.setValue(nil, forKey: "is-login")
                UserDefaults.standard.setValue(nil, forKey: "token")
                UserDefaults.standard.setValue(nil, forKey: "first_name")
                UserDefaults.standard.setValue(nil, forKey: "last_name")
                UserDefaults.standard.removeObject(forKey: "recent_search")
                UserDefaults.standard.synchronize()
                let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
                self.navigationController?.pushViewController(vc, animated: true)
             }
             else {
                let alertController = UIAlertController(title: "Alert", message: "Something went wrong.", preferredStyle:.alert)

                alertController.addAction(UIAlertAction(title: "OK", style: .default)
                { action -> Void in
                  UserDefaults.standard.setValue(nil, forKey: "is-login")
                  UserDefaults.standard.setValue(nil, forKey: "token")
                  UserDefaults.standard.setValue(nil, forKey: "first_name")
                  UserDefaults.standard.setValue(nil, forKey: "last_name")
                  UserDefaults.standard.removeObject(forKey: "recent_search")
                  UserDefaults.standard.synchronize()
                  let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                  let vc = storyboard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
                  self.navigationController?.pushViewController(vc, animated: true)
                })
                self.present(alertController, animated: true, completion: nil)
             }

         }
    }
    
    func ApiCallTogetUserDetails() {
        getMethodWithAuthorizationReturnJson(apiName: "my-profile/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                self.lblName.text = data["first_name"]?.stringValue
                self.lblEmail.text = data["email"]?.stringValue
                self.imgImage.image = UIImage(named: "temp_profile")
                self.imgImage.layer.cornerRadius = self.imgImage.frame.height/2
                self.txtMobile.text = data["phone"]!.stringValue
            }
        }
    }
    
    //    MARK:- View Cart
    func ApiCallToViewCart(){
        var auth : String?
        var deviceId : String
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        if UserDefaults.standard.value(forKey: "token") as? String != nil {
            auth = (UserDefaults.standard.value(forKey: "token") as! String)
            let headers :[String : Any] = [
                "Authorization": "Token \(auth!)",
                "Content-Type": "application/json",
                "WAREHOUSE": "\(wareHouseId)",
                "WID": "1",
                "DEVICEID": "\(deviceId)"
            ]
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers) { (response: JSON) in
                print(response)
                if response["status"].intValue == 200 {
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    print(self.badgeCount)
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
                else {
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
                
            }
        }
        else {
            let headers :[String : Any] = [
                "Content-Type": "application/json",
                "WAREHOUSE": "\(wareHouseId)",
                "WID": "1",
                "DEVICEID": "\(deviceId)"
            ]
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers) { (response: JSON) in
                print(response)
                if response["status"].intValue == 200 {
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
                else {
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
            }
        }
    }
    
    func ApiCallToGetCartCount(){
        var auth : String?
        var deviceId : String
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        if UserDefaults.standard.value(forKey: "token") as? String != nil {
            auth = (UserDefaults.standard.value(forKey: "token") as! String)
            let headers :[String : Any] = [
                "Authorization": "Token \(auth!)",
                "Content-Type": "application/json",
                "WAREHOUSE": "\(wareHouseId)",
                "WID": "1",
                "DEVICEID": "\(deviceId)"
            ]
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "cart-count/", vc: self, header: headers) { (response: JSON) in
                 print(response)
                if response["cart_count"].intValue > 0 {
                    self.ApiCallToViewCart()
                }
                else {
                    self.btnCartCount.isHidden = true
                     self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
            }
        }
        else {
            let headers :[String : Any] = [
                "Content-Type": "application/json",
                "WAREHOUSE": "\(wareHouseId)",
                "WID": "1",
                "DEVICEID": "\(deviceId)"
            ]
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers) { (response: JSON) in
                 print(response)
                if response["cart_count"].intValue > 0 {
                    self.ApiCallToViewCart()
                }
                else {
                    self.btnCartCount.isHidden = true
                     self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
                
            }
        }
    }
}


