
import UIKit
import SwiftyJSON
import FirebaseAnalytics
class CartViewController: UIViewController , UITextFieldDelegate{
    @IBOutlet weak var tableViewHeightConstant: NSLayoutConstraint!
    @IBOutlet weak var btbCheckout: UIButton!
    @IBOutlet weak var lblCartPrice: UILabel!
    @IBOutlet weak var lblTotalAmount: UILabel!
    @IBOutlet weak var lblSubTotal: UILabel!
    @IBOutlet weak var viewPrice: UIView!
    @IBOutlet weak var viewOrderSummary: UIView!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var orderSummaryHeight: NSLayoutConstraint!
    @IBOutlet weak var viewPriceHeight: NSLayoutConstraint!
    @IBOutlet weak var viewEmptyCart: UIView!
    @IBOutlet weak var viewEmptyCartheight: NSLayoutConstraint!
    @IBOutlet weak var btnShowNow: UIButton!
    @IBOutlet weak var viewCartAmount: UIView!
    @IBOutlet weak var btnCart: UIButton!
    @IBOutlet weak var btnCartCount: UIButton!
    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var txtNote: UITextField!
    @IBOutlet weak var viewNoteHeight: NSLayoutConstraint!
    @IBOutlet weak var viewNote: UIView!
    
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var cartArray = [JSON]()
    var cartDatafromDb = [AddcCart]()
    var badgeCount:Int = 0
    var navigationType:String = ""
    var minimumOrderAmount = Double()
    var orderAmount = Double()
    var Content_ID = String()
    var Content_Type = String()
    var Currency = String()
    var ValueToSum = String()
    var yearCheck = String()
    var contentNameArray = String()
    var contentIdArray = String()
    override func viewDidLoad() {
        super.viewDidLoad()
        
        txtNote.delegate = self
        viewCartAmount.addShadow1()
        navigationView.addShadow1()
        btnCartCount.layer.cornerRadius = btnCartCount.frame.height/2
        self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
        self.btbCheckout.layer.cornerRadius = 5
        self.btbCheckout.addShadow1()
        self.tableViewHeightConstant.constant = 100 * 25
        self.viewPrice.addShadow1()
        self.viewOrderSummary.addShadow1()
        self.txtNote.layer.cornerRadius = 5
        self.txtNote.setLeftPaddingPoints(10)
        txtNote.attributedPlaceholder = NSAttributedString(string: "Add a note to your order ",  attributes: [NSAttributedString.Key.foregroundColor: UIColor(displayP3Red: 81.0/255.0, green: 80.0/255.0, blue: 80.0/255.0, alpha: 1)])
        // Do any additional setup after loading the view.
    }
    
    
    @IBAction func btnSearchAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "SearchViewController") as! SearchViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.ApiCallToViewCart()
        //self.ApiCallToGetCartCount()
        self.navigationController?.setNavigationBarHidden(true, animated: true)
    }
    
    override func viewDidLayoutSubviews() {
    
    }
    
    @IBAction func btnCartAction(_ sender: Any) {
        
    }
    
    @IBAction func btnBackAction(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }

    //    MARK:- Button Action
    @objc func btncartAction() {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        self.navigationController?.pushViewController(vc, animated: true)
        
    }
    @objc func btnSearchAction() {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "SearchViewController") as! SearchViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    
    //    MARK:- Button Actions
    @objc func filterTapped() {
    }
    
    @IBAction func btnCheckOutAction(_ sender: Any) {
        if orderAmount >= minimumOrderAmount {
            CheckLogin()
        }
        else {
            createalert(title: "Alert", message: "Minimum Order Amount should be \(minimumOrderAmount)", vc: self)
        }
        
    }
    
    @objc func btnShopNowAction(sender:UIButton) {
        let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func CheckLogin() {
        if (UserDefaults.standard.value(forKey: "is-login") != nil){
            if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                ApiCallToGetCartSummary()
            }
            else {
                let storyboard:UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
                self.navigationController?.pushViewController(vc, animated: true)
            }
        }
        else {
            let storyboard:UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
            self.navigationController?.pushViewController(vc, animated: true)
        }
    }
    @objc func btnPlusAction(sender: UIButton) {
        var ageString = String()
        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
            ageString = ageCheckString as! String
              yearCheck = ageString
        }
        else {
            ageString = ""
            yearCheck = ageString
        }

        
        var coreDataindex = Int()
        var superview = sender.superview
        while let view = superview, !(view is UITableViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UITableViewCell else {
            print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = tableView.indexPath(for: cell) else {
            print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? CartTableViewCell else {
            print("rferffddvd")
            return
        }
        print(indexPath)
        // We've got the index path for the cell that contains the button, now do something with it.
        
        self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        let cartDict = self.cartArray[sender.tag].dictionaryValue
        
        let productDict = cartDict["product_id"]!.dictionaryValue
        
        var newProductId = String()
        var newQuantity = cartDict["quantity"]?.intValue
        let productId = "\(productDict["id"]!.intValue)"
        
        self.Content_ID = "\(productDict["id"]!.intValue)"
        self.Content_Type = cartDict["product_name"]!.stringValue
        self.ValueToSum = cartDict["new_default_price_unit"]!.stringValue
        
        let count = newQuantity! + 1
        for (index, element) in cartDatafromDb.enumerated() {
            print("Item \(index): \(element)")
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id
                let quantt = element.quantity!
                let quant1 = quantt
                print(quant1)
                var inttype: Int = Int(quantt)!
                print(inttype)
                if inttype > 0 {
                    print(inttype)
                    inttype = inttype + 1
                    newQuantity = inttype
                    cell1.btnMinus.isHidden = false
                    cell1.btnPlus.isHidden = false
                }
            }
        }
        if UserDefaults.standard.value(forKey: "token") as? String != nil {
            let auth = UserDefaults.standard.value(forKey: "token") as! String
            print(auth)
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = productId
            params["quantity"] = count
            params["Authorization"] = "Token \(auth)"
            params["warehouse_id"] = self.wareHouseId
              params["year_check"] = yearCheck
            // "Authorization": "Bearer \(auth)",
            print(params)
            postMethodQueryWithVc(apiName: "add-to-cart/", params: params, vc: self) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    print(count1)
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    print(cost)
                    let dict = ["cost":cost ,"product_id":"\(productId)","quantity":count] as [String : Any]
                    print(dict)
                    
                    cell1.btnAddtoCart.setTitle("\(count)", for: .normal)
                    cell1.btnPlus.isHidden = false
                    cell1.btnMinus.isHidden = false
                    cell1.btnAddtoCart.backgroundColor = .white
                    cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                    cell1.cartStack.layer.cornerRadius = 5
                    cell1.cartStack.clipsToBounds = true
                    cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1.cartStack.layer.borderWidth = 1
                    
                    //   DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    self.lblSubTotal.text = " "
                    self.lblCartPrice.text = " "
                    self.lblTotalAmount.text = " "
                    self.ApiCallToViewCart()
                     let contentName = cartDict["product_name"]?.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName!]
                    
                    print(dictParam)
                    AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.Content_ID)", content_Type: self.Content_Type, currency: "AED", valueToSum: self.ValueToSum)
                }
                else {
                    if response["is_age_verification"].stringValue == "False" {
                        requestAgeCheckView(vc: self)
                         AgeCheckView.lblText.text = response["msg"].stringValue
                      //     self.count = 0
                        AgeCheckView.viewEighteen.layer.shadowColor = UIColor.lightGray.cgColor
                        AgeCheckView.viewEighteen.layer.shadowOpacity = 1
                        AgeCheckView.viewEighteen.layer.shadowOffset = .zero
                        AgeCheckView.viewEighteen.layer.cornerRadius = 5
                        AgeCheckView.viewEighteen.layer.shadowRadius = 1
                        AgeCheckView.viewEighteen.layer.shadowPath = UIBezierPath(rect: AgeCheckView.viewEighteen.bounds).cgPath
                        AgeCheckView.viewEighteen.layer.shouldRasterize = true
                        AgeCheckView.viewEighteen.layer.rasterizationScale = UIScreen.main.scale
                        
                        AgeCheckView.btnAboveAge.addTarget(self,action:#selector(self.btnAboveAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnBelowAge.addTarget(self,action:#selector(self.btnBelowAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnAboveAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.addShadow1()
                        AgeCheckView.btnAboveAge.addShadow1()
                        AgeCheckView.viewEighteen.addShadow1()
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                      //  self.count = 0
                    }

                }
            }
        }
        else {
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = productId
            params["quantity"] = count
            params["warehouse_id"] = self.wareHouseId
              params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithVc(apiName: "add-to-cart/", params: params, vc: self) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    print(count1)
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    print(cost)
                    let dict = ["cost":cost ,"product_id":"\(productId)","quantity":count] as [String : Any]
                    print(dict)
                    
                    cell1.btnAddtoCart.setTitle("\(count)", for: .normal)
                    cell1.btnPlus.isHidden = false
                    cell1.btnMinus.isHidden = false
                    cell1.btnAddtoCart.backgroundColor = .white
                    cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                    cell1.cartStack.layer.cornerRadius = 5
                    cell1.cartStack.clipsToBounds = true
                    cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1.cartStack.layer.borderWidth = 1
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    print(DataBaseHelper.sharedInstance.getCartData())
                    print(self.cartDatafromDb.count)
                    self.lblSubTotal.text = " "
                    self.lblCartPrice.text = " "
                    self.lblTotalAmount.text = " "
                    //  self.cartArray.removeAll()
                    self.ApiCallToViewCart()
                    let contentName = cartDict["product_name"]?.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName!]
                    AddCart(dictParam: dictParam)
                    // self.tableView.reloadData()
                }
                else {
                    if response["is_age_verification"].stringValue == "False" {
                        requestAgeCheckView(vc: self)
                         AgeCheckView.lblText.text = response["msg"].stringValue
                        AgeCheckView.viewEighteen.layer.shadowColor = UIColor.lightGray.cgColor
                        AgeCheckView.viewEighteen.layer.shadowOpacity = 1
                        AgeCheckView.viewEighteen.layer.shadowOffset = .zero
                        AgeCheckView.viewEighteen.layer.cornerRadius = 5
                        AgeCheckView.viewEighteen.layer.shadowRadius = 1
                        AgeCheckView.viewEighteen.layer.shadowPath = UIBezierPath(rect: AgeCheckView.viewEighteen.bounds).cgPath
                        AgeCheckView.viewEighteen.layer.shouldRasterize = true
                        AgeCheckView.viewEighteen.layer.rasterizationScale = UIScreen.main.scale
                        
                        AgeCheckView.btnAboveAge.addTarget(self,action:#selector(self.btnAboveAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnBelowAge.addTarget(self,action:#selector(self.btnBelowAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnAboveAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.addShadow1()
                        AgeCheckView.btnAboveAge.addShadow1()
                        AgeCheckView.viewEighteen.addShadow1()
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                    }
                }
            }
        }
    }
    @objc func btnMinusAction(sender: UIButton) {
        
        var ageString = String()
        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
            ageString = ageCheckString as! String
              yearCheck = ageString
        }
        else {
            ageString = ""
            yearCheck = ageString
        }

        
        var coreDataindex = Int()
        var superview = sender.superview
        while let view = superview, !(view is UITableViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UITableViewCell else {
            print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = tableView.indexPath(for: cell) else {
            print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? CartTableViewCell else {
            print("rferffddvd")
            return
        }
        self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        print(DataBaseHelper.sharedInstance.getCartData())
        print(self.cartDatafromDb.count)
        
        
        
        let cartDict = self.cartArray[sender.tag].dictionaryValue
        print(cartDict)
        let productDict = cartDict["product_id"]!.dictionaryValue
        var newProductId = String()
        var newQuantity = cartDict["quantity"]?.intValue
        let productId = "\(productDict["id"]!.intValue)"
        
        self.Content_ID = "\(productDict["id"]!.intValue)"
        self.Content_Type = cartDict["product_name"]!.stringValue
        self.ValueToSum = cartDict["new_default_price_unit"]!.stringValue
        let count = newQuantity! - 1
        for (index, element) in cartDatafromDb.enumerated() {
            print("Item \(index): \(element)")
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id
                let quantt = element.quantity!
                let quant1 = quantt
                print(quant1)
                var inttype: Int = Int(quantt)!
                print(inttype)
                if inttype > 0 {
                    print(inttype)
                    inttype = inttype + 1
                    newQuantity = inttype
                    cell1.btnMinus.isHidden = false
                    cell1.btnPlus.isHidden = false
                }
            }
        }
        if UserDefaults.standard.value(forKey: "token") as? String != nil {
            let auth = UserDefaults.standard.value(forKey: "token") as! String
            print(auth)
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = productId
            params["quantity"] = count
            params["Authorization"] = "Token \(auth)"
            params["warehouse_id"] = self.wareHouseId
              params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithVc(apiName: "add-to-cart/", params: params, vc: self) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    if cartDict["cartdetails"]?.arrayValue.count == 0 {
                        print(self.cartDatafromDb.count)
                        cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                        cell1.btnMinus.isHidden = true
                        cell1.btnPlus.isHidden = true
                        self.cartArray.removeAll()
                        self.ApiCallToViewCart()
                        
                    }
                    else {
                        let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                        print(count1)
                        let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                        let count = "\(count1)"
                        let cost = "\(cost1)"
                        print(cost)
                        let dict = ["cost":cost ,"product_id":"\(productId)","quantity":count] as [String : Any]
                        print(dict)
                        print(DataBaseHelper.sharedInstance.getCartData())
                        print(self.cartDatafromDb.count)
                        
                        cell1.btnAddtoCart.setTitle("\(count)", for: .normal)
                        cell1.btnPlus.isHidden = false
                        cell1.btnMinus.isHidden = false
                        cell1.btnAddtoCart.backgroundColor = .white
                        cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                        cell1.cartStack.layer.cornerRadius = 5
                        cell1.cartStack.clipsToBounds = true
                        cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                        cell1.cartStack.layer.borderWidth = 1
                    }
                    print(DataBaseHelper.sharedInstance.getCartData())
                    print(self.cartDatafromDb.count)
                    self.lblSubTotal.text = " "
                    self.lblCartPrice.text = " "
                    self.lblTotalAmount.text = " "
                    self.ApiCallToViewCart()
                }
                else {
                    if response["is_age_verification"].stringValue == "False" {
                        requestAgeCheckView(vc: self)
                         AgeCheckView.lblText.text = response["msg"].stringValue
                        AgeCheckView.viewEighteen.layer.shadowColor = UIColor.lightGray.cgColor
                        AgeCheckView.viewEighteen.layer.shadowOpacity = 1
                        AgeCheckView.viewEighteen.layer.shadowOffset = .zero
                        AgeCheckView.viewEighteen.layer.cornerRadius = 5
                        AgeCheckView.viewEighteen.layer.shadowRadius = 1
                        AgeCheckView.viewEighteen.layer.shadowPath = UIBezierPath(rect: AgeCheckView.viewEighteen.bounds).cgPath
                        AgeCheckView.viewEighteen.layer.shouldRasterize = true
                        AgeCheckView.viewEighteen.layer.rasterizationScale = UIScreen.main.scale
                        AgeCheckView.btnAboveAge.addTarget(self,action:#selector(self.btnAboveAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnBelowAge.addTarget(self,action:#selector(self.btnBelowAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnAboveAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.addShadow1()
                        AgeCheckView.btnAboveAge.addShadow1()
                        AgeCheckView.viewEighteen.addShadow1()
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                    }
                }
            }
        }
        else {
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = productId
            params["quantity"] = count
            params["warehouse_id"] = self.wareHouseId
            params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithVc(apiName: "add-to-cart/", params: params, vc: self) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    if cartDict["cartdetails"]?.arrayValue.count == 0 {
                        cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                        cell1.btnMinus.isHidden = true
                        cell1.btnPlus.isHidden = true
                        self.cartArray.removeAll()
                        self.ApiCallToViewCart()
                    }
                    else {
                        let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                        print(count1)
                        let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                        let count = "\(count1)"
                        let cost = "\(cost1)"
                        print(cost)
                        let dict = ["cost":cost ,"product_id":"\(productId)","quantity":count] as [String : Any]
                        print(dict)
                        print(DataBaseHelper.sharedInstance.getCartData())
                        let contentName = cartDict["product_name"]?.stringValue
                        let dictParam :[String:Any] = ["Content_ID":"\(self.Content_ID)","Content_Type":self.Content_Type,"Currency":"AED","ValueToSum":self.ValueToSum]
                        print(dictParam)
                    }
                    print(DataBaseHelper.sharedInstance.getCartData())
                    print(self.cartDatafromDb.count)
                    self.lblSubTotal.text = " "
                    self.lblCartPrice.text = " "
                    self.lblTotalAmount.text = " "
                    self.ApiCallToViewCart()
                }
                else {
                    if response["is_age_verification"].stringValue == "False" {
                        requestAgeCheckView(vc: self)
                         AgeCheckView.lblText.text = response["msg"].stringValue
                        AgeCheckView.viewEighteen.layer.shadowColor = UIColor.lightGray.cgColor
                        AgeCheckView.viewEighteen.layer.shadowOpacity = 1
                        AgeCheckView.viewEighteen.layer.shadowOffset = .zero
                        AgeCheckView.viewEighteen.layer.cornerRadius = 5
                        AgeCheckView.viewEighteen.layer.shadowRadius = 1
                        AgeCheckView.viewEighteen.layer.shadowPath = UIBezierPath(rect: AgeCheckView.viewEighteen.bounds).cgPath
                        AgeCheckView.viewEighteen.layer.shouldRasterize = true
                        AgeCheckView.viewEighteen.layer.rasterizationScale = UIScreen.main.scale
                        
                        AgeCheckView.btnAboveAge.addTarget(self,action:#selector(self.btnAboveAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnBelowAge.addTarget(self,action:#selector(self.btnBelowAgeAction) , for: .touchUpInside)
                        AgeCheckView.btnAboveAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.layer.cornerRadius = 5
                        AgeCheckView.btnBelowAge.addShadow1()
                        AgeCheckView.btnAboveAge.addShadow1()
                        AgeCheckView.viewEighteen.addShadow1()
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                       // self.count = 0
                    }

                }
            }
        }
    }
    
    @objc func btnAboveAgeAction(sender:UIButton) {
        UserDefaults.standard.setValue("Y", forKey: "Age_Check")
        UserDefaults.standard.synchronize()
        AgeCheckView.removeFromSuperview()
    }
    @objc func btnBelowAgeAction(sender:UIButton) {
        UserDefaults.standard.setValue("N", forKey: "Age_Check")
        UserDefaults.standard.synchronize()
        AgeCheckView.removeFromSuperview()
    }
    //    MARK:- Api Calling
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
            print(headers)
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers) { (response: JSON) in
                print(response)
                if response["msg"].stringValue == "Success" {
                    self.minimumOrderAmount = response["minimum_order_amount"].doubleValue
                    self.orderAmount = response["total_amount"].doubleValue
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    print(self.badgeCount)
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    let tt = response["total_amount"].doubleValue
                    print(tt)
                    let lblSubTotal = String(format: "%.2f", tt) // "3.14"
                    self.lblSubTotal.text = "AED \(lblSubTotal)"
                    self.lblSubTotal.font = UIFont(name: "hind-semibold", size: 16)
                    self.lblSubTotal.font = .boldSystemFont(ofSize: 16)
                    let lblCartPrice = response["total_amount"].doubleValue
                    let lblCartPrice1 = String(format: "%.2f", lblCartPrice)
                    self.lblCartPrice.text = "AED \(lblCartPrice1)"
                    self.lblCartPrice.font = UIFont(name: "hind-semibold", size: 16)
                    self.lblCartPrice.font = .boldSystemFont(ofSize: 16)
                    let lblTotalAmount = response["total_amount"].doubleValue
                    let lblTotalAmount1 = String(format: "%.2f", lblTotalAmount)
                    self.lblTotalAmount.text = "AED \(lblTotalAmount1)"
                    self.lblTotalAmount.font = UIFont(name: "hind-semibold", size: 16)
                    self.lblTotalAmount.font = .boldSystemFont(ofSize: 16)
                    self.tableViewHeightConstant.constant = CGFloat(self.cartArray.count * 100)
                    self.tableView.delegate = self
                    self.tableView.dataSource = self
                    self.tableView.reloadData()
                    self.viewDidLayoutSubviews()
                    self.viewCartAmount.isHidden = false
                    self.viewNoteHeight.constant = 50
                    self.viewNote.isHidden = false
                }
                else {
                    self.tableViewHeightConstant.constant = 0
                    self.orderSummaryHeight.constant = 0
                    self.viewPrice.isHidden = true
                    self.viewPriceHeight.constant = 0
                    self.lblCartPrice.isHidden = true
                    self.btbCheckout.isHidden = true
                    self.viewOrderSummary.isHidden = true
                    self.viewEmptyCart.isHidden = false
                    self.btnShowNow.layer.cornerRadius = 5
                    self.btnShowNow.addShadow2()
                    self.btnShowNow.isUserInteractionEnabled = true
                    self.btnShowNow.addTarget(self, action: #selector(self.btnShopNowAction), for: .touchUpInside)
                    self.tableView.delegate = self
                    self.tableView.dataSource = self
                    self.tableView.reloadData()
                    self.badgeCount = 0
                    self.viewDidLayoutSubviews()
                    self.viewCartAmount.isHidden = true
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    self.viewNoteHeight.constant = 0
                    self.viewNote.isHidden = true
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
            print(headers)
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers) { (response: JSON) in
                print(response)
                if response["msg"].stringValue == "Success" {
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    print(self.badgeCount)
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    
                    let tt = response["total_amount"].doubleValue
                    let lblSubTotal = String(format: "%.2f", tt) // "3.14"
                    self.lblSubTotal.text = "AED \(lblSubTotal)"
                    
                    self.lblSubTotal.font = UIFont(name: "hind-semibold", size: 16)
                    self.lblSubTotal.font = .boldSystemFont(ofSize: 16)
                    let lblCartPrice = response["total_amount"].doubleValue
                    let lblCartPrice1 = String(format: "%.2f", lblCartPrice)
                    self.lblCartPrice.text = "AED \(lblCartPrice1)"
                    self.lblCartPrice.font = UIFont(name: "hind-semibold", size: 16)
                    self.lblCartPrice.font = .boldSystemFont(ofSize: 16)
                    
                    let lblTotalAmount = response["total_amount"].doubleValue
                    let lblTotalAmount1 = String(format: "%.2f", lblTotalAmount)
                    self.lblTotalAmount.text = "AED \(lblTotalAmount1)"
                    self.lblTotalAmount.font = UIFont(name: "hind-semibold", size: 16)
                    self.lblTotalAmount.font = .boldSystemFont(ofSize: 16)
                    
                    self.tableViewHeightConstant.constant = CGFloat(self.cartArray.count * 100)
                    self.tableView.delegate = self
                    self.tableView.dataSource = self
                    self.tableView.reloadData()
                    self.viewDidLayoutSubviews()
                    self.viewCartAmount.isHidden = false
                    self.viewNoteHeight.constant = 50
                    self.viewNote.isHidden = false
                }
                else {
                    self.tableViewHeightConstant.constant = 0
                    self.orderSummaryHeight.constant = 0
                    self.viewPrice.isHidden = true
                    self.viewPriceHeight.constant = 0
                    self.lblCartPrice.isHidden = true
                    self.btbCheckout.isHidden = true
                    self.viewOrderSummary.isHidden = true
                    self.viewEmptyCart.isHidden = false
                    self.viewEmptyCart.addShadow2()
                    self.btnShowNow.layer.cornerRadius = 5
                    self.btnShowNow.addShadow2()
                    self.btnShowNow.isUserInteractionEnabled = true
                    self.btnShowNow.addTarget(self, action: #selector(self.btnShopNowAction), for: .touchUpInside)
                    self.badgeCount = 0
                    self.viewDidLayoutSubviews()
                    self.viewCartAmount.isHidden = true
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    self.viewNoteHeight.constant = 0
                    self.viewNote.isHidden = true
                    
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
                    self.tableViewHeightConstant.constant = 0
                    self.orderSummaryHeight.constant = 0
                    self.viewPrice.isHidden = true
                    self.viewPriceHeight.constant = 0
                    self.lblCartPrice.isHidden = true
                    self.btbCheckout.isHidden = true
                    self.viewOrderSummary.isHidden = true
                    self.viewEmptyCart.isHidden = false
                    self.viewEmptyCart.addShadow2()
                    self.btnShowNow.layer.cornerRadius = 5
                    self.btnShowNow.addShadow2()
                    self.btnShowNow.isUserInteractionEnabled = true
                    self.btnShowNow.addTarget(self, action: #selector(self.btnShopNowAction), for: .touchUpInside)
                    self.badgeCount = 0
                    self.viewDidLayoutSubviews()
                    self.viewCartAmount.isHidden = true
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    self.viewNoteHeight.constant = 0
                    self.viewNote.isHidden = true
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
                    self.tableViewHeightConstant.constant = 0
                    self.orderSummaryHeight.constant = 0
                    self.viewPrice.isHidden = true
                    self.viewPriceHeight.constant = 0
                    self.lblCartPrice.isHidden = true
                    self.btbCheckout.isHidden = true
                    self.viewOrderSummary.isHidden = true
                    self.viewEmptyCart.isHidden = false
                    self.viewEmptyCart.addShadow2()
                    self.btnShowNow.layer.cornerRadius = 5
                    self.btnShowNow.addShadow2()
                    self.btnShowNow.isUserInteractionEnabled = true
                    self.btnShowNow.addTarget(self, action: #selector(self.btnShopNowAction), for: .touchUpInside)
                    self.badgeCount = 0
                    self.viewDidLayoutSubviews()
                    self.viewCartAmount.isHidden = true
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    self.viewNoteHeight.constant = 0
                    self.viewNote.isHidden = true
                }
                
            }
        }
    }
    
    func  ApiCallToGetCartSummary() {
        if txtNote.text?.isEmpty == false {
            UserDefaults.standard.setValue(txtNote.text ?? "", forKey: "addNote")
            UserDefaults.standard.synchronize()
        }
        else {
            UserDefaults.standard.setValue("", forKey: "addNote")
            UserDefaults.standard.synchronize()
        }
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        var params = [String:Any]()
        params["warehouse_id"] = wareHouseId
        params["special_instructions"] = self.txtNote.text ?? ""
        postMethodQuery2(apiName: "cart-summary/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                let cartData = response["data"].dictionaryValue
                let cartDetailsArr = cartData["cartdetails"]?.arrayValue
                for index in cartDetailsArr! {
                    let contentName = index["name"].stringValue
                    self.contentNameArray = self.contentNameArray  + contentName + ", "
                    let contentId = "\(index["id"].intValue)"
                    self.contentIdArray = self.contentIdArray  + contentId + ", "
                }
                
                let content_ids = self.contentIdArray
                let content_name = self.contentNameArray
                let content_type = "product_group"
                let num_items  = cartDetailsArr?.count ?? 0
                let value = self.lblTotalAmount.text!
                let currency  = "AED"
                let dictParam :[String:Any] = ["Content_ID":"\(content_ids)","Content_Type":content_type,"Content_Name":content_name,"num_items":num_items,"Value_To_Sum":value,"Currency":currency]
                Checkout(dictParam: dictParam)

                logInitiateCheckoutEvent(contentIds: self.contentIdArray, contentName:  self.contentNameArray, contentType: "product_group", numItems: "\(cartDetailsArr?.count ?? 0)", value: self.lblTotalAmount.text!, currency: "AED")
                   self.ApiCallToGetAddressList()
            }
            else {
                createalert(title: "Alert", message: response["msg"].stringValue, vc: self)
            }
        }
    }
    
    func ApiCallToGetAddressList() {
        getMethodWithAuthorizationReturnJsonWithoutDeviceId(apiName: "delivery-address/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                let addressArray = response["data"].arrayValue
                if addressArray.count != 0 {
                    let vc = self.storyboard?.instantiateViewController(withIdentifier: "DeliveryDetailsViewController") as! DeliveryDetailsViewController
                    let backButton = UIBarButtonItem()
                    backButton.title = ""
                    self.navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
                    self.navigationController?.pushViewController(vc, animated: true)
                }
                else {
                    let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveAddressViewController") as! SaveAddressViewController
                    vc.pageType = "Cart"
                    self.navigationController?.pushViewController(vc, animated: true)
                }
            }
        }
        
    }
//    MARK:- Textfield Delegate
    
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
        let whitespaceSet = NSCharacterSet.whitespaces
        let range1 = string.rangeOfCharacter(from: whitespaceSet)
        if let _ = range1 {
            let txt = textField.text ?? ""
            if txt.isBlankByTrimming || txt.isEmpty {
                return false
            } else if textField.text?.last == " "  && string == " "{

            // If consecutive spaces entered by user
             return false
            }
            else {
                return true
            }
        }
        else {
            return true
        }
        
        
    }
}
extension CartViewController : UITableViewDelegate , UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        self.cartArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "CartTableViewCell", for: indexPath) as! CartTableViewCell
        
        //DispatchQueue.main.async {
        let cartDict = self.cartArray[indexPath.row].dictionaryValue
        cell.lblTitle.text = cartDict["product_name"]?.stringValue
        // cell.lblTitle.font = UIFont(name: "hind-bold", size: 16)
        cell.lblTitle.font = .boldSystemFont(ofSize: 16)
        let price = cartDict["new_default_price_unit"]!.doubleValue
        let doubleStr = String(format: "%.2f", price) // "3.14"
        print(doubleStr)
        cell.lblOrignalPrice.text = "AED \(doubleStr)"
        cell.lblOrignalPrice.font = .boldSystemFont(ofSize: 15)
        let productIdDict = cartDict["product_id"]?.dictionaryValue
        if (productIdDict!["product_image"]!["img"].string)!.isEmpty == false {
            let productImageurl = productIdDict!["product_image"]!["img"].stringValue
            let fullUrl = IMAGE_PRODUCT_URL + productImageurl
            let url = URL(string: fullUrl)
            print(url!)
            cell.imgProduct.sd_setImage(with: url!)
        }
        else {
            cell.imgProduct.image = UIImage(named:"no_image")
            cell.imgProduct.image?.withAlignmentRectInsets(UIEdgeInsets(top: -25, left: -25, bottom: -25, right: -25))
        }
        cell.btnAddtoCart.layer.cornerRadius = 5
        let quantity = cartDict["quantity"]!.intValue
        if quantity != 0 {
            cell.btnAddtoCart.setTitle("\(quantity)", for: .normal)
            cell.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 16)
            cell.btnAddtoCart.titleLabel?.font = .boldSystemFont(ofSize: 16)
            cell.btnAddtoCart.backgroundColor = .white
            cell.btnAddtoCart.setTitleColor(.black, for: .normal)
            cell.cartStack.layer.cornerRadius = 5
            cell.cartStack.clipsToBounds = true
            cell.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
            cell.cartStack.layer.borderWidth = 1
            
            cell.btnPlus.isHidden = false
            cell.btnMinus.isHidden = false
        }
        cell.plusMinusStack.layer.borderColor = UIColor.green.cgColor
        cell.plusMinusStack.layer.borderWidth = 1
        cell.btnPlus.tag = indexPath.row
        cell.btnPlus.addTarget(self, action: #selector(self.btnPlusAction), for: .touchUpInside)
        cell.btnMinus.tag = indexPath.row
        cell.btnMinus.addTarget(self, action: #selector(self.btnMinusAction), for: .touchUpInside)
        //   }
        return cell
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let cartDict = self.cartArray[indexPath.row].dictionaryValue
        print(cartDict)
        let slug = cartDict["product_slug"]?.stringValue
        let productIdDict = cartDict["product_id"]?.dictionaryValue
        let productIdInCart = productIdDict!["id"]!.intValue
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
        vc.slugInDetail = slug!
        //        vc.productIdInDetail = productIdInCart
        print(productIdInCart)
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 99
    }
}
extension String {
    var isBlankByTrimming: Bool {
              let trimmed = self.trimmingCharacters(in:
                  CharacterSet.whitespacesAndNewlines)
                    return trimmed.isEmpty
                 }
     func trimWhitespacesAndNewlines() -> String{
           return self.trimmingCharacters(in:
                             CharacterSet.whitespacesAndNewlines)
     }
    
}
