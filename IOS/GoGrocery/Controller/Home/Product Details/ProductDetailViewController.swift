
import UIKit
import SwiftyJSON
import FirebaseAnalytics
class ProductDetailViewController: UIViewController {
    @IBOutlet weak var btnMinus: UIButton!
    @IBOutlet weak var btnPlus: UIButton!
    @IBOutlet weak var btnWishListDetail: UIButton!
    @IBOutlet weak var btnAddToCartDetail: UIButton!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var cartStack: UIView!
    @IBOutlet weak var cartWishListView: UIView!
    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var btnShare: UIButton!
    @IBOutlet weak var btnWishList: UIButton!
    @IBOutlet weak var btnCartCount: UIButton!
    @IBOutlet weak var btnCart: UIButton!
    var slugInDetail = String()
    var productDetailDict = [String:JSON]()
    var similarProductId = Int()
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var count = Int()
    var quantity = Int()
    var productId = Int()
    var cartDatafromDb = [AddcCart]()
    var cartArray = [JSON]()
    var badgeCount = Int()
    var prId = 0
    var productIdArr = [Int]()
    var isAddedToWishList = false
    var wishListImgName = "saveList"
    var screenSize: CGRect!
    var screenWidth: CGFloat!
    var screenHeight: CGFloat!
    private let spacing:CGFloat = 0
    var similarProductDictAr = [[String:Any]]()
    var bestSellingProductDictAr = [[String:Any]]()
    var heightForSimilarProductRow = 0
    var heightForBestSellingProductRow = 0
    var ratingData = [JSON]()
    var reviewData = [JSON]()
    var ratingAvg = Double()
    var totalRow = 5
    var isShowAllReview = false
    var similarArray = [JSON]()
    var bestSellingArray = [JSON]()
    var Content_ID = String()
     var Content_Type = String()
     var Currency = String()
     var ValueToSum = String()
     var yearCheck = String()
    var productImageArray = [JSON]()
    //    MARK:- View Life Cycle
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        cartWishListView.addShadow1()
        btnCartCount.layer.cornerRadius = btnCartCount.frame.height/2
        navigationView.addShadow1()
        tableView.contentInsetAdjustmentBehavior = .never
        print("productid-- \(prId)")
        self.count = 0
        self.btnWishListDetail.layer.cornerRadius = 5
        self.btnAddToCartDetail.layer.cornerRadius = 5
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        cartStack.layer.cornerRadius = 5
        cartStack.clipsToBounds = true
        cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        cartStack.layer.borderWidth = 1
        cartStack.addShadow2()
        btnWishListDetail.addShadow2()
        // ApiCallToGetProductDetail()
       // apiCallToWishList()
        
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
        ApiCallToGetProductDetail()
        self.ApiCallToGetCartCount(isLoader: false)
        self.apiCallToWishList()

    }
    override func viewDidLayoutSubviews() {
    }
    
    // MARK: - Button Actions
    // MARK: -
    @IBAction func btnCartAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnWishListAction(_ sender: Any) {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let productId = self.productDetailDict["id"]!.intValue
            print(self.productDetailDict)
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveListViewController") as! SaveListViewController
            vc.productId = productId
            self.navigationController?.pushViewController(vc, animated: true)
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
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
    
    @IBAction func btnShareAction(_ sender: Any) {
        print("Share functionality not available")
    }
    @IBAction func btnBackAction(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    @IBAction func btnAddToCartDetailAction(_ sender: Any) {
        
        
        var ageString = String()
        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
            ageString = ageCheckString as! String
             yearCheck = ageString
        }
        else {
            ageString = ""
             yearCheck = ageString
        }
            self.count = count + 1
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            if UserDefaults.standard.value(forKey: "token") as? String != nil {
                let auth = UserDefaults.standard.value(forKey: "token") as! String
                print(auth)
                var params = [String:Any]()
                params["device_id"] = deviceID
                params["product_id"] = self.productId
                params["quantity"] = self.count
                params["Authorization"] = "Token \(auth)"
                params["year_check"] = yearCheck
                print(params)
                postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                    print(response)
                    if response["status"].intValue == 1 {
                        let cartDict = response["cart_data"].dictionaryValue
                        let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                        print(count1)
                        let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                        let count = "\(count1)"
                        let cost = "\(cost1)"
                        print(cost)
                        let dict = ["cost":cost ,"product_id":"\(self.productId)","quantity":count] as [String : Any]
                        self.btnAddToCartDetail.setTitle("\(count)", for: .normal)
                        self.btnPlus.isHidden = false
                        self.btnMinus.isHidden = false
                        self.btnAddToCartDetail.backgroundColor = .white
                        self.btnAddToCartDetail.setTitleColor(.black, for: .normal)
                        self.cartStack.layer.cornerRadius = 5
                        self.cartStack.clipsToBounds = true
                        self.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                        self.cartStack.layer.borderWidth = 1

                        DataBaseHelper.sharedInstance.save(object: dict)
                        self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                        print(DataBaseHelper.sharedInstance.getCartData())
                        print(self.cartDatafromDb.count)
                        self.count = 0
                        self.ApiCallToGetCartCount(isLoader: true)
                       // self.ApiCallToViewCart()
                        
                        let contentName = self.productDetailDict["name"]!.stringValue
                        let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                     
                        print(dictParam)
                        AddCart(dictParam: dictParam)
                        logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
                    }
                    else {
//                        self.btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
//                        self.btnPlus.isHidden = true
//                        self.btnMinus.isHidden = true
//                        self.count = 0
                            if response["is_age_verification"].stringValue == "False" {
                                
                            if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                                self.count = 0
                            }
                            else {
                                requestAgeCheckView(vc: self)
                                 AgeCheckView.lblText.text = response["msg"].stringValue
                                  self.count = 0
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
                        }
                        else {
                            let msg = response["msg"].stringValue
                            createalert(title: "Alert", message: msg, vc: self)
                            self.count = 0
                        }

                    }
                }
            }
            else {
                var params = [String:Any]()
                params["device_id"] = deviceID
                params["product_id"] = self.productId
                params["quantity"] = self.count
                params["year_check"] = yearCheck
                print(params)
                postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                    print(response)
                    if response["status"].intValue == 1 {
                        let cartDict = response["cart_data"].dictionaryValue
                        let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                        print(count1)
                        let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                        let count = "\(count1)"
                        let cost = "\(cost1)"
                        print(cost)
                        let dict = ["cost":cost ,"product_id":"\(self.productId)","quantity":count] as [String : Any]
                        self.btnAddToCartDetail.setTitle("\(count)", for: .normal)
                        self.btnAddToCartDetail.backgroundColor = .white
                        self.btnAddToCartDetail.setTitleColor(.black, for: .normal)
                        self.btnMinus.isHidden = false
                        self.btnPlus.isHidden = false
                        self.cartStack.layer.cornerRadius = 5
                        DataBaseHelper.sharedInstance.save(object: dict)
                        self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                        print(DataBaseHelper.sharedInstance.getCartData())
                        print(self.cartDatafromDb.count)
                        self.count = 0
                      self.ApiCallToGetCartCount(isLoader: true)
                        //self.ApiCallToViewCart()
                        let contentName = self.productDetailDict["name"]!.stringValue
                        let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                      //  let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":"\(cost)"]
                        print(dictParam)
                        AddCart(dictParam: dictParam)
                        logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
                    }
                    else {
//                        self.btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
//                        self.btnPlus.isHidden = true
//                        self.btnMinus.isHidden = true
//                        self.count = 0
                            if response["is_age_verification"].stringValue == "False" {
                                
                            if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                                self.count = 0
                            }
                            else {
                                requestAgeCheckView(vc: self)
                                 AgeCheckView.lblText.text = response["msg"].stringValue
                                  self.count = 0
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
                        }
                        else {
                            let msg = response["msg"].stringValue
                            createalert(title: "Alert", message: msg, vc: self)
                            self.count = 0
                        }
                    }
                }
            }
       // }
    }
    
    @IBAction func btnminusAction(_ sender: Any) {
        
        var ageString = String()
         if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
             ageString = ageCheckString as! String
              yearCheck = ageString
         }
         else {
             ageString = ""
              yearCheck = ageString
         }
         
         
        var newProductId = String()
        var newQuantity = Int()
        var coreDataindex = Int()
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        print(DataBaseHelper.sharedInstance.getCartData())
        print(cartDatafromDb)
        let productId =  "\(self.productDetailDict["stock_data"]!["product_id"].intValue)"
        for (index, element) in cartDatafromDb.enumerated() {
            print("Item \(index): \(element)")
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                let quant1 = quantt
                print(quant1)
                var inttype: Int = Int(quantt)!
                print(inttype)
                print(inttype)
                inttype = inttype - 1
                newQuantity = inttype
                btnMinus.isHidden = false
                btnPlus.isHidden = false
            }
            else {
                btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
                btnMinus.isHidden = true
                btnPlus.isHidden = true
            }
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        if UserDefaults.standard.value(forKey: "token") as? String != nil {
            let auth = UserDefaults.standard.value(forKey: "token") as! String
            print(auth)
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = newProductId
            params["quantity"] = newQuantity
            params["Authorization"] = "Token \(auth)"
            params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    print(count1)
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    print(cost)
                    let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                    self.btnAddToCartDetail.setTitle("\(newQuantity)", for: .normal)
                    self.btnPlus.isHidden = false
                    self.btnMinus.isHidden = false
                    self.cartStack.layer.cornerRadius = 5
                    if count1 == 0 {
                        DataBaseHelper.sharedInstance.delete(index: coreDataindex)
                        self.btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
                        self.btnPlus.isHidden = true
                        self.btnMinus.isHidden = true
                        self.btnAddToCartDetail.backgroundColor = UIColor(named: "buttonBackgroundColor")
                        self.btnAddToCartDetail.setTitleColor(.white, for: .normal)
                        self.cartStack.layer.cornerRadius = 5
                        self.cartStack.clipsToBounds = true
                        self.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                        self.cartStack.layer.borderWidth = 1
                    }
                    else {
                        DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                    }
                    print(dict)
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    print(DataBaseHelper.sharedInstance.getCartData())
                    print(self.cartDatafromDb.count)
                    self.ApiCallToGetCartCount(isLoader: true)
                   // self.ApiCallToViewCart()
                    let contentName = self.productDetailDict["name"]!.stringValue
                   // let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":cost]
                    //print(dictParam)
                    //self.ReduceCart(dictParam: dictParam)
                }
                else {
                        if response["is_age_verification"].stringValue == "False" {
                            
                        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                            self.count = 0
                        }
                        else {
                            requestAgeCheckView(vc: self)
                             AgeCheckView.lblText.text = response["msg"].stringValue
                              self.count = 0
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
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                        self.count = 0
                    }
                }
            }
        }
        else {
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = newProductId
            params["quantity"] = newQuantity
            params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    print(count1)
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    print(cost)
                    let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                    self.btnAddToCartDetail.setTitle("\(newQuantity)", for: .normal)
                    self.btnPlus.isHidden = false
                    self.btnMinus.isHidden = false
                    self.cartStack.layer.cornerRadius = 5
                    if count1 == 0 {
                        DataBaseHelper.sharedInstance.delete(index: coreDataindex)
                        self.btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
                        self.btnPlus.isHidden = true
                        self.btnMinus.isHidden = true
                        self.btnAddToCartDetail.backgroundColor = UIColor(named: "buttonBackgroundColor")
                        self.btnAddToCartDetail.setTitleColor(.white, for: .normal)
                        self.cartStack.layer.cornerRadius = 5
                        self.cartStack.clipsToBounds = true
                        self.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                        self.cartStack.layer.borderWidth = 1
                    }
                    else {
                        DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                    }
                    print(dict)
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    self.ApiCallToGetCartCount(isLoader: true)
                   // self.ApiCallToViewCart()
                    let contentName = self.productDetailDict["name"]!.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":cost]
                    print(dictParam)
                   // self.ReduceCart(dictParam: dictParam)
                }
                else {
                        if response["is_age_verification"].stringValue == "False" {
                            
                        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                            self.count = 0
                        }
                        else {
                            requestAgeCheckView(vc: self)
                             AgeCheckView.lblText.text = response["msg"].stringValue
                              self.count = 0
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
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                        self.count = 0
                    }
                }
            }
        }
    }
    @IBAction func btnAddAction(_ sender: Any) {
        var ageString = String()
         if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
             ageString = ageCheckString as! String
              yearCheck = ageString
         }
         else {
             ageString = ""
              yearCheck = ageString
         }
         
         
        var newProductId = String()
        var newQuantity = Int()
        var coreDataindex = Int()
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        print(DataBaseHelper.sharedInstance.getCartData())
        print(cartDatafromDb)
        let productId =  "\(self.productDetailDict["stock_data"]!["product_id"].intValue)"
        for (index, element) in cartDatafromDb.enumerated() {
            print("Item \(index): \(element)")
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                let quant1 = quantt
                print(quant1)
                var inttype: Int = Int(quantt)!
                print(inttype)
                print(inttype)
                inttype = inttype + 1
                newQuantity = inttype
                btnMinus.isHidden = false
                btnPlus.isHidden = false
            }
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        if UserDefaults.standard.value(forKey: "token") as? String != nil {
            let auth = UserDefaults.standard.value(forKey: "token") as! String
            print(auth)
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = newProductId
            params["quantity"] = newQuantity
            params["Authorization"] = "Token \(auth)"
            params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    print(count1)
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    print(cost)
                    let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                    self.btnAddToCartDetail.setTitle("\(newQuantity)", for: .normal)
                    self.btnAddToCartDetail.backgroundColor = .white
                    self.btnAddToCartDetail.setTitleColor(.black, for: .normal)
                    self.btnMinus.isHidden = false
                    self.btnPlus.isHidden = false
                    self.cartStack.layer.cornerRadius = 5
                    print(dict)
                      self.ApiCallToGetCartCount(isLoader: true)
                    DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                    //checkBool = false
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    print(DataBaseHelper.sharedInstance.getCartData())
                    print(self.cartDatafromDb.count)
                    self.viewDidLayoutSubviews()
                    let contentName = self.productDetailDict["name"]!.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                    AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
                }
                else {
//                    let msg = response["msg"].stringValue
//                    createalert(title: "Alert", message: msg, vc: self)
                        if response["is_age_verification"].stringValue == "False" {
                            
                        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                            self.count = 0
                        }
                        else {
                            requestAgeCheckView(vc: self)
                             AgeCheckView.lblText.text = response["msg"].stringValue
                              self.count = 0
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
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                        self.count = 0
                    }
                }
            }
        }
        else {
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = newProductId
            params["quantity"] = newQuantity
            params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    print(count1)
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    print(cost)
                    let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                    self.btnAddToCartDetail.setTitle("\(newQuantity)", for: .normal)
                    self.btnAddToCartDetail.backgroundColor = .white
                    self.btnAddToCartDetail.setTitleColor(.black, for: .normal)
                    self.btnMinus.isHidden = false
                    self.btnPlus.isHidden = false
                    self.cartStack.layer.cornerRadius = 5
                    print(dict)
                      self.ApiCallToGetCartCount(isLoader: true)
                    DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    print(DataBaseHelper.sharedInstance.getCartData())
                    print(self.cartDatafromDb.count)
                    self.viewDidLayoutSubviews()
                    let contentName = self.productDetailDict["name"]!.stringValue
                   // let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":"\(cost)"]
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                    print(dictParam)
                    AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
                }
                else {
//                    let msg = response["msg"].stringValue
//                    createalert(title: "Alert", message: msg, vc: self)
                        if response["is_age_verification"].stringValue == "False" {
                            
                        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                            self.count = 0
                        }
                        else {
                            requestAgeCheckView(vc: self)
                             AgeCheckView.lblText.text = response["msg"].stringValue
                              self.count = 0
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
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                        self.count = 0
                    }
                }
            }
        }
    }
    @IBAction func btnWishListDetailAction(_ sender: Any) {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            if self.isAddedToWishList == true {
                deleteFromWishList()
            } else {
                addToWishList()
                
            }
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
        }
    }
    @objc func btnManufactureByAction() {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
        let slug = productDetailDict["category"]!["slug"].stringValue
        vc.slugInListing = slug
        self.navigationController?.pushViewController(vc, animated: true)   
    }
    
    func addToWishList() {
        var params = [String:Any]()
        params["product_id"] = prId
        params["website_id"] = 1
        postMethodQuery2(apiName: "my-wish-list/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                DispatchQueue.main.async {
                    self.wishListImgName = "wish_select"
                    self.viewDidLayoutSubviews()
                    self.isAddedToWishList = true
                    createalert(title: "Alert", message: "Successfully added to wishlist", vc: self)
                    self.btnWishListDetail.setTitle("  SAVED", for: .normal)
                    self.btnWishListDetail.setImage(UIImage(named: "wish_select"), for: .normal)
                    
                    let contentName = self.productDetailDict["name"]!.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(self.prId)","Content_Type":"product","Content_Name":contentName]
                    print(dictParam)
                    AddToWishlist(dictParam: dictParam)
                    logAdd_to_wishlistEvent(content_ID: "\(self.Content_ID)", content_Type: self.Content_Type, currency: "AED", valueToSum: "")
                }
            }
            else {
                let msg = response["msg"].stringValue
                createalert(title: "Alert", message: msg, vc: self)
            }
        }
    }
    
    func deleteFromWishList() {
        let productId = "\(prId)"
        var params = [String:Any]()
        params["product_id"] = productId
        postMethodQuery2(apiName: "delete-wishlist/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                DispatchQueue.main.async {
                    self.wishListImgName = "wish_select"
                    self.viewDidLayoutSubviews()
                    self.isAddedToWishList = false
                    createalert(title: "Alert", message: "Successfully removed from wishlist", vc: self)
                    self.btnWishListDetail.setTitle("  WISHLIST", for: .normal)
                    self.btnWishListDetail.setImage(UIImage(named: "wish_select"), for: .normal)
                   // let contentName = self.productDetailDict["name"]!.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(self.Content_ID)","Content_Type":self.Content_Type,"Currency":"AED","ValueToSum":"\(self.ValueToSum)"]
                    print(dictParam)
                  //  self.RemoveFromWishlist(dictParam: dictParam)
                    
                }
            }
            else {
                let msg = response["msg"].stringValue
                createalert(title: "Alert", message: msg, vc: self)
            }
        }
    }
    
    //    MARK:- View Cart
    func ApiCallToViewCart(isdismiss:Bool = false ){
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
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers,isDismiss: isdismiss) { (response: JSON) in
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
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers,isDismiss: isdismiss) { (response: JSON) in
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
    
    func ApiCallToGetCartCount(isLoader:Bool){
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
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "cart-count/", vc: self, header: headers,isDismiss: isLoader) { (response: JSON) in
                print(response)
                if response["cart_count"].intValue > 0 {
                    self.ApiCallToViewCart(isdismiss: true)
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
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers,isDismiss: isLoader) { (response: JSON) in
                print(response)
                if response["cart_count"].intValue > 0 {
                   self.ApiCallToViewCart(isdismiss: true)
                }
                else {
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
                
            }
        }
    }
    
    //MARK:- Api Calling
    func apiCallToWishList() {
        if UserDefaults.standard.value(forKey: "token") != nil {
            let auth = UserDefaults.standard.value(forKey: "token") as! String
            let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
            let headers:[String : Any] = ["Authorization": "Token \(auth)","WID":"\(wareHouseId)","website_id":"1" , "Content-Type": "application/json"]
            getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "my-wish-list/", vc: self, header: headers,isDismiss: false) { (response) in
                print(response)
                if response["status"].stringValue == "200" {
                    let data = response["data"].arrayValue
                    for product in data {
                        let productDict = product["product"].dictionaryValue
                        self.productIdArr.append(productDict["id"]!.intValue)
                    }
                    if self.productIdArr.contains(self.prId) {
                        DispatchQueue.main.async {
                            self.wishListImgName = "wish_select"
                            self.btnWishListDetail.setImage(UIImage(named: "wish_select"), for: .normal)
                            self.viewDidLayoutSubviews()
                            self.isAddedToWishList = true
                            self.btnWishListDetail.setTitle("  SAVED", for: .normal)
                            self.btnWishListDetail.setImage(UIImage(named: "wish_select"), for: .normal)
                        }
                    } else {
                        DispatchQueue.main.async {
                            self.wishListImgName = "wish_select"
                            self.viewDidLayoutSubviews()
                            self.isAddedToWishList = false
                            self.btnWishListDetail.setImage(UIImage(named: "wish_select"), for: .normal)
                            self.btnWishListDetail.setTitle("  WISHLIST", for: .normal)
                        }
                    }
                }
                else {
                    
                    //createalert(title: "Alert", message: "Something went wrong , please try after sometime", vc: self)
                }
            }
        }
        
    }
    func ApiCallToGetProductDetail() {
        let headers :[String : Any] = [
            // "Authorization": "Bearer \(auth)",
            "Content-Type": "application/json",
            "WAREHOUSE": "\(wareHouseId)",
            "WID": "1"
        ]
        print(headers)
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "product-details/\(slugInDetail)", vc: self, header: headers,isDismiss: false) { (response: JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.productDetailDict = response["data"].dictionaryValue
                print( self.productDetailDict)
                self.productId = self.productDetailDict["stock_data"]!["product_id"].intValue
                
                let contentName = self.productDetailDict["name"]?.string ?? ""
                let content_category = self.productDetailDict["category"]?["name"].string ?? ""
                let content_ids = self.productDetailDict["id"]?.int ?? 0
                let content_type = "product"
                let value = self.productDetailDict["default_price"]?.int ?? 0
                let currency = "AED"
             let dictParam :[String:Any] = ["Content_Name":"\(contentName)","Content_Category":content_category,"Content_Id":"\(content_ids)","content_type":"\(content_type)","ValueToSum":value , "currency":currency]
                 ViewProduct(dictParam: dictParam)
                
                self.similarProductId = self.productDetailDict["id"]!.intValue
                self.ApiCallToGetSimilarProduct()
                self.ApiCallToGetBestSellingProduct()
                //  self.ApiCallToGetRateReview()
                print(self.productDetailDict)
                let productID = "\(self.productDetailDict["stock_data"]!["product_id"].intValue)"
                self.Content_ID = "\(self.productDetailDict["stock_data"]!["product_id"].intValue)"
                let catName = self.productDetailDict["category"]!["name"].stringValue
                let price = "\(self.productDetailDict["default_price"]?.doubleValue ?? 0.00)"
                let name = self.productDetailDict["name"]?.stringValue
                if self.productDetailDict["product_image"]?.arrayValue.count != 0 {
                    let productImagesArr = self.productDetailDict["product_image"]?.arrayValue
                    self.productImageArray = productImagesArr!
                }
                logViewProductDetailEvent(contentName: name!, contentCategory: catName, contentIds: "\(self.productId)", content_type: "product", value: price, currency: "AED")
                for index in self.cartDatafromDb {
                    if productID == index.product_id {
                        if let quant = index.quantity {
                            //let costt = index.cost!
                            let inttype: Int = Int(quant) ?? 0
                            print(inttype)
                            if inttype != 0 {
                                DispatchQueue.main.async {
                                    self.btnAddToCartDetail.setTitle("\(inttype)", for: .normal)
                                    self.btnAddToCartDetail.backgroundColor = .white
                                    self.btnAddToCartDetail.setTitleColor(.black, for: .normal)
                                    self.btnMinus.isHidden = false
                                    self.btnPlus.isHidden = false
                                    self.cartStack.layer.cornerRadius = 5
                                    self.cartStack.clipsToBounds = true
                                    self.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                                    self.cartStack.layer.borderWidth = 1
                                    print(inttype)
                                    
                                    
                                    
//                                    self.btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
//                                     self.btnPlus.isHidden = true
//                                     self.btnMinus.isHidden = true
//                                     self.btnAddToCartDetail.backgroundColor = UIColor(named: "buttonBackgroundColor")
//                                     self.btnAddToCartDetail.setTitleColor(.white, for: .normal)
//                                     self.cartStack.layer.cornerRadius = 5
//                                     self.cartStack.clipsToBounds = true
//                                     self.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
//                                     self.cartStack.layer.borderWidth = 1
                                    
                                }
                            }
                            else {
                                self.btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
                                self.btnAddToCartDetail.backgroundColor = .clear
                                self.btnAddToCartDetail.setTitleColor(.white, for: .normal)
                                self.btnMinus.isHidden = true
                                self.btnPlus.isHidden = true
                                self.cartStack.layer.cornerRadius = 5
                            }
                        }
                    }
                    else {
                        self.btnAddToCartDetail.setTitle("ADD TO CART", for: .normal)
                        self.btnAddToCartDetail.backgroundColor = .clear
                        self.btnAddToCartDetail.setTitleColor(.white, for: .normal)
                        self.btnMinus.isHidden = true
                        self.btnPlus.isHidden = true
                        self.cartStack.layer.cornerRadius = 5
                    }
                }
                self.tableView.delegate = self
                self.tableView.dataSource = self
                self.tableView.reloadData()
            }
            else {
                
            }
        }
    }
    func ApiCallToGetSimilarProduct(){
        var deviceId : String
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        let headers :[String : Any] = [
            "Content-Type": "application/json",
            "WAREHOUSE": "\(wareHouseId)",
            "DEVICEID": deviceId
        ]
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "similar-product/\(self.similarProductId)/", vc: self, header: headers,isDismiss: true) { (response: JSON) in
            print("sim1")
            print(response)
            // self.ApiCallToGetBestSellingProduct()
            if response["status"].intValue == 200 {
                self.similarProductDictAr.removeAll()
                let dataAr = response["data"].arrayValue
                self.similarArray = response["data"].arrayValue
                for data in dataAr {
                    var productDict = [String:Any]()
                    let product = data["product"].dictionaryValue
                    productDict["name"] = product["name"]?.stringValue
                    productDict["weight"] = product["weight"]?.stringValue
                    productDict["price"] = product["new_default_price"]?.doubleValue
                    productDict["id"] = product["id"]?.intValue
                    productDict["slug"] = product["slug"]?.stringValue
                    let imgAr = product["product_image"]?.arrayValue
                    if let imageAr = imgAr {
                        if imageAr.count > 0 {
                            let imageDict = imageAr[0]
                            productDict["image"] = imageDict["img"].stringValue
                        } else {
                            productDict["image"] = ""
                        }
                    } else {
                        productDict["image"] = ""
                    }
                    
                    self.similarProductDictAr.append(productDict)
                }
                var totalProduct = Int()
                if self.similarProductDictAr.count > 6 {
                    totalProduct = 6
                }
                else {
                    totalProduct = self.similarProductDictAr.count
                }
                if totalProduct % 2 == 0 {
                    self.heightForSimilarProductRow = (totalProduct / 2)*340 + 44
                } else {
                    self.heightForSimilarProductRow = ((totalProduct / 2) + 1)*340 + 44
                }
                self.tableView.reloadData()
            }
            else {
                print("similar product empty")
            }
        }
    }
    
    func ApiCallToGetBestSellingProduct(){
        var deviceId : String
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        
        let headers :[String : Any] = [
            "Content-Type": "application/json",
            "WAREHOUSE": "\(wareHouseId)",
            "DEVICEID": deviceId
        ]
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "popular-product/\(self.similarProductId)/", vc: self, header: headers,isDismiss: false) { (response: JSON) in
            print("sim1")
            print(response)
            if response["status"].intValue == 200 {
                self.bestSellingProductDictAr.removeAll()
                let dataAr = response["data"].arrayValue
                self.bestSellingArray = response["data"].arrayValue
                for data in dataAr {
                    var productDict = [String:Any]()
                    print(data)
                    let product = data["product"].dictionaryValue
                    productDict["name"] = product["name"]?.stringValue
                    productDict["weight"] = product["weight"]?.stringValue
                    productDict["price"] = product["new_default_price"]?.doubleValue
                    productDict["id"] = product["id"]?.intValue
                    productDict["slug"] = product["slug"]?.stringValue
                    let brandDict = product["brand"]?.dictionaryValue
                    productDict["brand"] = brandDict!["name"]?.stringValue
                    let imgAr = product["product_image"]?.arrayValue
                    if let imageAr = imgAr {
                        if imageAr.count > 0 {
                            let imageDict = imageAr[0]
                            productDict["image"] = imageDict["img"].stringValue
                        } else {
                            productDict["image"] = ""
                        }
                    } else {
                        productDict["image"] = ""
                    }
                    self.bestSellingProductDictAr.append(productDict)
                }
                var totalProduct = Int()
                if self.bestSellingProductDictAr.count > 6 {
                    totalProduct = 6
                }
                else {
                    totalProduct = self.similarProductDictAr.count
                }
                if totalProduct % 2 == 0 {
                    self.heightForBestSellingProductRow = (totalProduct / 2)*350 + 40
                }
                else {
                    self.heightForBestSellingProductRow = ((totalProduct / 2) + 1)*350 + 40
                }
                self.tableView.reloadData()
            }
            else {
                print("Best product empty")
            }
        }
    }
    
    
    //    MARK:- Button Actions
    @objc func addToCartbtnAction(sender: UIButton) {
        
        var ageString = String()
         if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
             ageString = ageCheckString as! String
              yearCheck = ageString
         }
         else {
             ageString = ""
              yearCheck = ageString
         }
//
//        if ageString == "N" {
//
//        }
//        else {
            self.count = count + 1
            print(similarProductDictAr[sender.tag])
            let cell: SimilarProductTableViewCell? = (self.tableView.cellForRow(at: IndexPath.init(row: totalRow-2, section: 0)) as! SimilarProductTableViewCell)
            let cell1: SimilarProductCollectionViewCell? = (cell?.similarProductCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! SimilarProductCollectionViewCell)
            let productDict = similarProductDictAr[sender.tag]
            // let sourceDict = productDict["_source"]?.dictionaryValue
            productId = productDict["id"] as! Int
            quantity = count
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var auth = String()
            if (UserDefaults.standard.value(forKey: "is-login") != nil){
                auth = (UserDefaults.standard.value(forKey: "token") as! String)
            }
            else {
                auth = " "
            }
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = productId
            params["quantity"] = quantity
            params["Authorization"] = "Token \(auth)"
            params["year_check"] = yearCheck
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    cell1?.btnAddtoCart.setTitle("\(count)", for: .normal)
                    cell1?.btnPlus.isHidden = false
                    cell1?.btnMinus.isHidden = false
                    cell1?.btnAddtoCart.backgroundColor = .white
                    cell1?.btnAddtoCart.setTitleColor(.black, for: .normal)
                    cell1?.cartStack.layer.cornerRadius = 5
                    cell1?.cartStack.clipsToBounds = true
                    cell1?.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1?.cartStack.layer.borderWidth = 1
                    let dict = ["cost":cost ,"product_id":"\(self.productId)","quantity":count] as [String : Any]
                    DataBaseHelper.sharedInstance.save(object: dict)
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    self.count = 0
                    self.cartArray.removeAll()
                    self.ApiCallToGetCartCount(isLoader: true)
                 //   self.ApiCallToViewCart()
                    let productDict = self.similarProductDictAr[sender.tag]
                    let contentName = productDict["name"] as! String
                    //let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":"\(cost)"]
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                    print(dictParam)
                    AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
                }
                else {
//                    cell1?.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
//                    cell1?.btnPlus.isHidden = true
//                    cell1?.btnMinus.isHidden = true
//                    cell1?.cartStack.layer.cornerRadius = 5
//                    cell1?.cartStack.clipsToBounds = true
//                    let msg = response["msg"].stringValue
//                    createalert(title: "Alert", message: msg, vc: self)
//                    self.count = 0
                        if response["is_age_verification"].stringValue == "False" {
                            
                        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                            self.count = 0
                        }
                        else {
                            requestAgeCheckView(vc: self)
                             AgeCheckView.lblText.text = response["msg"].stringValue
                              self.count = 0
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
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                        self.count = 0
                    }

                }
            }
     //   }
         

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
         
         
        var newProductId = String()
        var newQuantity = Int()
        var coreDataindex = Int()
        let cell: SimilarProductTableViewCell? = (self.tableView.cellForRow(at: IndexPath.init(row: totalRow-2, section: 0)) as! SimilarProductTableViewCell)
        let cell1: SimilarProductCollectionViewCell? = (cell?.similarProductCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! SimilarProductCollectionViewCell)
        let productDict = similarProductDictAr[sender.tag]
        let productId = "\(productDict["id"] as! Int)"
        for (index, element) in cartDatafromDb.enumerated() {
            //print("Item \(index): \(element)")
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                var inttype: Int = Int(quantt)!
                print(inttype)
                inttype = inttype + 1
                newQuantity = inttype
            }
        }
        
        var auth = String()
        if (UserDefaults.standard.value(forKey: "is-login") != nil){
            auth = (UserDefaults.standard.value(forKey: "token") as! String)
        }
        else {
            auth = " "
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
        params["device_id"] = deviceID
        params["product_id"] = newProductId
        params["quantity"] = newQuantity
        params["Authorization"] = "Token \(auth)"
            params["year_check"] = yearCheck
        postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
                cell1?.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
                cell1?.btnPlus.isHidden = false
                cell1?.btnMinus.isHidden = false
                cell1?.btnAddtoCart.backgroundColor = .white
                cell1?.btnAddtoCart.setTitleColor(.black, for: .normal)
                cell1?.cartStack.layer.cornerRadius = 5
                cell1?.cartStack.clipsToBounds = true
                cell1?.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                cell1?.cartStack.layer.borderWidth = 1
                
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                self.cartArray.removeAll()
                self.ApiCallToGetCartCount(isLoader: true)
              //  self.ApiCallToViewCart()
                let productDict = self.similarProductDictAr[sender.tag]
                let contentName = productDict["name"] as! String
                //let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":"\(cost)"]
                let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                print(dictParam)
                AddCart(dictParam: dictParam)
                logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
            }
            else {
//                let msg = response["msg"].stringValue
//                createalert(title: "Alert", message: msg, vc: self)
                    if response["is_age_verification"].stringValue == "False" {
                        
                    if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                        self.count = 0
                    }
                    else {
                        requestAgeCheckView(vc: self)
                         AgeCheckView.lblText.text = response["msg"].stringValue
                          self.count = 0
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
                }
                else {
                    let msg = response["msg"].stringValue
                    createalert(title: "Alert", message: msg, vc: self)
                    self.count = 0
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
         
         
        var newProductId = String()
        var newQuantity = Int()
        var coreDataindex = Int()
        var tempCost = String()
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        let cell: SimilarProductTableViewCell? = (self.tableView.cellForRow(at: IndexPath.init(row: totalRow-2, section: 0)) as! SimilarProductTableViewCell)
        let cell1: SimilarProductCollectionViewCell? = (cell?.similarProductCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! SimilarProductCollectionViewCell)
        let productDict = similarProductDictAr[sender.tag]
        let productId = "\(productDict["id"] as! Int)"
        for (index, element) in cartDatafromDb.enumerated() {
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                var inttype: Int = Int(quantt)!
                inttype = inttype - 1
                newQuantity = inttype
                cell1?.btnMinus.isHidden = false
                cell1?.btnPlus.isHidden = false
                tempCost = element.cost
            }
            else {
                cell1?.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                cell1?.btnMinus.isHidden = true
                cell1?.btnPlus.isHidden = true
            }
        }
        var auth = String()
        if (UserDefaults.standard.value(forKey: "is-login") != nil){
            auth = (UserDefaults.standard.value(forKey: "token") as! String)
        }
        else {
            auth = " "
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
        params["device_id"] = deviceID
        params["product_id"] = newProductId
        params["quantity"] = newQuantity
        params["Authorization"] = "Token \(auth)"
            params["year_check"] = yearCheck
        postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                cell1?.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
                cell1?.btnPlus.isHidden = false
                cell1?.btnMinus.isHidden = false
                if count1 == 0 {
                    DataBaseHelper.sharedInstance.delete(index: coreDataindex)
                    cell1?.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                    cell1?.btnPlus.isHidden = true
                    cell1?.btnMinus.isHidden = true
                    cell1?.lblOrignalPrice.text = "AED \(tempCost)"
                    cell1?.btnAddtoCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
                    cell1?.btnAddtoCart.setTitleColor(.white, for: .normal)
                    cell1?.cartStack.layer.cornerRadius = 5
                    cell1?.cartStack.clipsToBounds = true
                    cell1?.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1?.cartStack.layer.borderWidth = 1
                    let productDict = self.similarProductDictAr[sender.tag]
                    let contentName = productDict["name"] as! String
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":cost]
                    print(dictParam)
                   // self.ReduceCart(dictParam: dictParam)
                }
                else {
                    let productDict = self.similarProductDictAr[sender.tag]
                    let contentName = productDict["name"] as! String
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":cost]
                    print(dictParam)
                   // self.ReduceCart(dictParam: dictParam)
                    DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                }
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                self.cartArray.removeAll()
                self.ApiCallToGetCartCount(isLoader: true)
               // self.ApiCallToViewCart()
            }
            else {
//                let msg = response["msg"].stringValue
//                createalert(title: "Alert", message: msg, vc: self)
                    if response["is_age_verification"].stringValue == "False" {
                        
                    if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                        self.count = 0
                    }
                    else {
                        requestAgeCheckView(vc: self)
                         AgeCheckView.lblText.text = response["msg"].stringValue
                          self.count = 0
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
                }
                else {
                    let msg = response["msg"].stringValue
                    createalert(title: "Alert", message: msg, vc: self)
                    self.count = 0
                }
            }
        }
    }
    
    //   MARK:- Cart Action for Best Selling
    @objc func btnAddToCartInBestbtnAction(sender:UIButton) {
        var ageString = String()
         if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
             ageString = ageCheckString as! String
              yearCheck = ageString
         }
         else {
             ageString = ""
              yearCheck = ageString
         }
//        if ageString == "N" {
//
//        }
//        else {
            self.count = count + 1
            let cell: BestSellingInProductTableViewCell? = (self.tableView.cellForRow(at: IndexPath.init(row: totalRow-1, section: 0)) as! BestSellingInProductTableViewCell)
            let cell1: BestSellingProductCollectionViewCell? = (cell?.bestCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! BestSellingProductCollectionViewCell)
            let productDict = bestSellingProductDictAr[sender.tag]
            productId = productDict["id"] as! Int
            quantity = count
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var auth = String()
            if (UserDefaults.standard.value(forKey: "is-login") != nil){
                auth = (UserDefaults.standard.value(forKey: "token") as! String)
            }
            else {
                auth = " "
            }
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = productId
            params["quantity"] = quantity
            params["Authorization"] = "Token \(auth)"
                params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    cell1?.btnAddToCart.setTitle("\(count)", for: .normal)
                    cell1?.btnPlus.isHidden = false
                    cell1?.btnMinus.isHidden = false
                    cell1?.btnAddToCart.backgroundColor = .white
                    cell1?.btnAddToCart.setTitleColor(.black, for: .normal)
                    cell1?.cartView.layer.cornerRadius = 5
                    cell1?.cartView.clipsToBounds = true
                    cell1?.cartView.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1?.cartView.layer.borderWidth = 1
                    let dict = ["cost":cost ,"product_id":"\(self.productId)","quantity":count] as [String : Any]
                    DataBaseHelper.sharedInstance.save(object: dict)
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    self.count = 0
                    self.cartArray.removeAll()
                    self.ApiCallToGetCartCount(isLoader: true)
                   // self.ApiCallToViewCart()
                    let productDict = self.bestSellingProductDictAr[sender.tag]
                    let contentName = productDict["name"] as! String
                   let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                    //let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":"\(cost)"]
                    print(dictParam)
                   AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
                }
                else {
//                    cell1?.btnAddToCart.setTitle("ADD TO CART", for: .normal)
//                    cell1?.btnPlus.isHidden = true
//                    cell1?.btnMinus.isHidden = true
//                    cell1?.cartView.layer.cornerRadius = 5
//                    cell1?.cartView.clipsToBounds = true
//                    let msg = response["msg"].stringValue
//                    createalert(title: "Alert", message: msg, vc: self)
//                    self.count = 0
                        if response["is_age_verification"].stringValue == "False" {
                            
                        if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                            self.count = 0
                        }
                        else {
                            requestAgeCheckView(vc: self)
                             AgeCheckView.lblText.text = response["msg"].stringValue
                              self.count = 0
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
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                        self.count = 0
                    }

                }
            }
     //   }
         
         

    }
    
    @objc func btnPlusInBestAction(sender:UIButton) {
        var ageString = String()
         if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
             ageString = ageCheckString as! String
              yearCheck = ageString
         }
         else {
             ageString = ""
              yearCheck = ageString
         }
         
        var newProductId = String()
        var newQuantity = Int()
        var coreDataindex = Int()
        let cell: BestSellingInProductTableViewCell? = (self.tableView.cellForRow(at: IndexPath.init(row: totalRow-1, section: 0)) as! BestSellingInProductTableViewCell)
        let cell1: BestSellingProductCollectionViewCell? = (cell?.bestCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! BestSellingProductCollectionViewCell)
        let productDict = bestSellingProductDictAr[sender.tag]
        let productId = "\(productDict["id"] as! Int)"
        for (index, element) in cartDatafromDb.enumerated() {
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                var inttype: Int = Int(quantt)!
                print(inttype)
                inttype = inttype + 1
                newQuantity = inttype
            }
        }
        var auth = String()
        if (UserDefaults.standard.value(forKey: "is-login") != nil){
            auth = (UserDefaults.standard.value(forKey: "token") as! String)
        }
        else {
            auth = " "
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
        params["device_id"] = deviceID
        params["product_id"] = newProductId
        params["quantity"] = newQuantity
        params["Authorization"] = "Token \(auth)"
            params["year_check"] = yearCheck
        postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
                cell1?.btnAddToCart.setTitle("\(newQuantity)", for: .normal)
                cell1?.btnPlus.isHidden = false
                cell1?.btnMinus.isHidden = false
                cell1?.btnAddToCart.backgroundColor = .white
                cell1?.btnAddToCart.setTitleColor(.black, for: .normal)
                cell1?.cartView.layer.cornerRadius = 5
                cell1?.cartView.clipsToBounds = true
                cell1?.cartView.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                cell1?.cartView.layer.borderWidth = 1
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                self.cartArray.removeAll()
                
                 self.ApiCallToGetCartCount(isLoader: true)
              //  self.ApiCallToViewCart()
                let productDict = self.bestSellingProductDictAr[sender.tag]
                  let contentName = productDict["name"] as! String
                  let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                 // let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":"\(cost)"]
                  print(dictParam)
                  AddCart(dictParam: dictParam)
                logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
            }
            else {
//                let msg = response["msg"].stringValue
//                createalert(title: "Alert", message: msg, vc: self)
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
                    self.count = 0
                }
            }
        }
    }
    
    @objc func btnMinusInBestAction(sender:UIButton) {
        var ageString = String()
         if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
             ageString = ageCheckString as! String
              yearCheck = ageString
         }
         else {
             ageString = ""
              yearCheck = ageString
         }
         
        var newProductId = String()
        var newQuantity = Int()
        var coreDataindex = Int()
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        let cell: BestSellingInProductTableViewCell? = (self.tableView.cellForRow(at: IndexPath.init(row: totalRow-1, section: 0)) as! BestSellingInProductTableViewCell)
        let cell1: BestSellingProductCollectionViewCell? = (cell?.bestCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! BestSellingProductCollectionViewCell)
        let productDict = bestSellingProductDictAr[sender.tag]
        let productId = "\(productDict["id"] as! Int)"
        for (index, element) in cartDatafromDb.enumerated() {
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                var inttype: Int = Int(quantt)!
                inttype = inttype - 1
                newQuantity = inttype
                cell1?.btnMinus.isHidden = false
                cell1?.btnPlus.isHidden = false
            }
            else {
                cell1?.btnAddToCart.setTitle("ADD TO CART", for: .normal)
                cell1?.btnMinus.isHidden = true
                cell1?.btnPlus.isHidden = true
            }
        }
        var auth = String()
        if (UserDefaults.standard.value(forKey: "is-login") != nil){
            auth = (UserDefaults.standard.value(forKey: "token") as! String)
        }
        else {
            auth = " "
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
        params["device_id"] = deviceID
        params["product_id"] = newProductId
        params["quantity"] = newQuantity
        params["Authorization"] = "Token \(auth)"
        params["year_check"] = yearCheck
        postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                cell1?.btnAddToCart.setTitle("\(newQuantity)", for: .normal)
                cell1?.btnPlus.isHidden = false
                cell1?.btnMinus.isHidden = false
                if count1 == 0 {
                    DataBaseHelper.sharedInstance.delete(index: coreDataindex)
                    cell1?.btnAddToCart.setTitle("ADD TO CART", for: .normal)
                    cell1?.btnPlus.isHidden = true
                    cell1?.btnMinus.isHidden = true
                    cell1?.btnAddToCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
                    cell1?.btnAddToCart.setTitleColor(.white, for: .normal)
                    cell1?.cartView.layer.cornerRadius = 5
                    cell1?.cartView.clipsToBounds = true
                    cell1?.cartView.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1?.cartView.layer.borderWidth = 1
                }
                else {
                    DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                }
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                self.cartArray.removeAll()
                 self.ApiCallToGetCartCount(isLoader: true)
             //   self.ApiCallToViewCart()
                let productDict = self.bestSellingProductDictAr[sender.tag]
                  let contentName = productDict["name"] as! String
                  let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":cost]
                  print(dictParam)
                 // self.ReduceCart(dictParam: dictParam)
            }
            else {
//                let msg = response["msg"].stringValue
//                createalert(title: "Alert", message: msg, vc: self)
                    if response["is_age_verification"].stringValue == "False" {
                        
                    if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
                        self.count = 0
                    }
                    else {
                        requestAgeCheckView(vc: self)
                         AgeCheckView.lblText.text = response["msg"].stringValue
                          self.count = 0
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
                }
                else {
                    let msg = response["msg"].stringValue
                    createalert(title: "Alert", message: msg, vc: self)
                    self.count = 0
                }
            }
        }
    }
    
    @objc func addToSaveListAction(sender: UIButton) {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let tag = sender.tag
            let productDict = similarProductDictAr[tag]
            let productId = productDict["id"] as! Int
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveListViewController") as! SaveListViewController
            vc.productId = productId
            self.navigationController?.pushViewController(vc, animated: true)
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
        }
    }
    
    @objc func addToSaveListBestAction(sender: UIButton) {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let tag = sender.tag
            let productDict = bestSellingProductDictAr[tag]
            let productId = productDict["id"] as! Int
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveListViewController") as! SaveListViewController
            vc.productId = productId
            self.navigationController?.pushViewController(vc, animated: true)
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
        }
    }
    @objc func viewAllReview(sender: UIButton) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ViewAllReviewViewController") as! ViewAllReviewViewController
        vc.allReviewData = self.reviewData
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @objc func rateProduct(sender: UIButton) {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "RateProductViewController") as! RateProductViewController
            vc.productId = self.prId
            self.navigationController?.pushViewController(vc, animated: true)
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
        }
        
    }

}
extension ProductDetailViewController : UITableViewDelegate , UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return totalRow
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        var commonCell = UITableViewCell()
        if indexPath.row == 0 {
            let cell1 = tableView.dequeueReusableCell(withIdentifier: "ProductImageTableViewCell") as! ProductImageTableViewCell
//            if productDetailDict["product_image"]?.arrayValue.count != 0 {
//                let productImagesArr = productDetailDict["product_image"]?.arrayValue
//                self.productImageArray = productImagesArr!
//            }
            commonCell = cell1
            
        }
        else  if indexPath.row == 1 {
            let cell2 = tableView.dequeueReusableCell(withIdentifier: "ProductNameTableViewCell") as! ProductNameTableViewCell
            if productDetailDict["brand"]?.dictionary?.isEmpty == false {
                let brandDict = productDetailDict["brand"]?.dictionaryValue
                let brand = brandDict!["name"]?.stringValue
                cell2.lblBrandName.text = brand
                cell2.lblBrandName.isHidden = false
            }
            else {
                let categoryString = productDetailDict["category"]!["name"].stringValue
                cell2.lblBrandName.text = categoryString
                cell2.lblBrandName.isHidden = false
            }
            if let categoryString = productDetailDict["category"]!["name"].string {
                cell2.btnCat.setTitle("\(categoryString)", for: .normal)
                cell2.lblCat.isHidden = false
                cell2.btnCat.isHidden = false
                cell2.btnCat.addTarget(self, action: #selector(btnManufactureByAction), for: .touchUpInside)
            }
            else {
                cell2.lblCat.isHidden = true
                cell2.btnCat.isHidden = true
            }
            cell2.lblProductName.text = productDetailDict["name"]!.stringValue
            cell2.lblSku.text = "SKU : \(productDetailDict["sku"]!.stringValue)"
            cell2.lblBrandName.isHidden = false
            self.Content_Type = productDetailDict["name"]!.stringValue
            commonCell = cell2
        }
        else if indexPath.row == 2 {
            let cell3 = tableView.dequeueReusableCell(withIdentifier: "ProductPriceTableViewCell") as! ProductPriceTableViewCell
            print(productDetailDict)
            let dd = String(format: "%.2f", productDetailDict["new_default_price_unit"]!.doubleValue)
            cell3.lblProductprice.text = "AED \(dd)"
            self.ValueToSum = "\(dd)"
            if let weight = productDetailDict["weight"]?.string {
                if let unit = productDetailDict["uom"]?.string {
                    cell3.lblProductWeight.text = "\(weight)\(unit)"
                    cell3.lblProductWeight.isHidden = false
                }
                else {
                    cell3.lblProductWeight.isHidden = true
                }
            }
            else {
                cell3.lblProductWeight.isHidden = true
            }
            if productDetailDict["discount_amount"]!.intValue != 0 {
                let sp = "AED \(productDetailDict["discount_amount"]!.intValue)"
                let attributeString: NSMutableAttributedString =  NSMutableAttributedString(string: sp)
                attributeString.addAttribute(NSAttributedString.Key.strikethroughStyle, value: 2, range: NSMakeRange(0, attributeString.length))
                cell3.lblStrikedPrice.attributedText = attributeString
                cell3.lblStrikedPrice.isHidden = false
                cell3.lblStrikedWidth.constant = 50
            }
            else {
                cell3.lblStrikedPrice.isHidden = true
                cell3.lblStrikedWidth.constant = 0
            }
            commonCell = cell3
        }
        else  if indexPath.row == 3 {
            guard let cell = self.tableView.dequeueReusableCell(withIdentifier: "SimilarProductTableViewCell", for: indexPath) as? SimilarProductTableViewCell else { fatalError("cell return null") }
            cell.backgroundColor = #colorLiteral(red: 0.9644367887, green: 0.9760565091, blue: 0.9760565091, alpha: 0.505721831)
            commonCell = cell
        }
        else  if indexPath.row == 4 {
            guard let cell = self.tableView.dequeueReusableCell(withIdentifier: "BestSellingInProductTableViewCell", for: indexPath) as? BestSellingInProductTableViewCell else { fatalError("cell return null") }
            cell.backgroundColor = #colorLiteral(red: 0.9644367887, green: 0.9760565091, blue: 0.9760565091, alpha: 0.505721831)
            commonCell = cell
        }
        return commonCell
    }
    
    func tableView(_ tableView: UITableView, willDisplay cell: UITableViewCell, forRowAt indexPath: IndexPath) {
        if indexPath.row == 0 {
            if let cell = cell as? ProductImageTableViewCell {
                cell.imgCollection.tag = 2
                cell.imgCollection.dataSource = self
                cell.imgCollection.delegate = self
                cell.imgCollection.reloadData()
            }
        }
        if indexPath.row == 3 {
            if let cell = cell as? SimilarProductTableViewCell {
                cell.similarProductCollectionView.tag = 0
                cell.similarProductCollectionView.dataSource = self
                cell.similarProductCollectionView.delegate = self
                cell.similarProductCollectionView.reloadData()
            }
        }
        if indexPath.row == 4 {
            if let cell = cell as? BestSellingInProductTableViewCell {
                cell.bestCollectionView.tag = 1
                cell.bestCollectionView.dataSource = self
                cell.bestCollectionView.delegate = self
                cell.bestCollectionView.reloadData()
            }
        }
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        var height : CGFloat
        if indexPath.row == 0 {
            height = 240
        }
        else if indexPath.row == 1 {
            height = 120
        }
        else if indexPath.row == 2 {
            height = 90
        }
        else if indexPath.row == 3 {
            height = CGFloat(self.heightForSimilarProductRow)
        }
        else if indexPath.row == 4 {
            height = CGFloat(self.heightForBestSellingProductRow)
        }
        else {
            return 0
        }
        
        return height
    }
    
    func tableView(_ tableView: UITableView, estimatedHeightForRowAt indexPath: IndexPath) -> CGFloat
    {
        var height : CGFloat
        
        if indexPath.row == 0 {
            height = 240
        }
        else if indexPath.row == 1 {
            height = 120
        }
        else if indexPath.row == 2 {
            height = 90
        }
        else if indexPath.row == 3 {
            height = CGFloat(self.heightForSimilarProductRow)
        }
        else if indexPath.row == 4 {
            height = CGFloat(self.heightForBestSellingProductRow)
        }
        else {
            height = 0
        }
        return height
    }
    
}

extension ProductDetailViewController : UICollectionViewDataSource , UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        if collectionView.tag == 0 {
            if self.similarProductDictAr.count > 6 {
                return 6
            }
            else {
                return similarProductDictAr.count
            }
        }
           else if collectionView.tag == 2 {
                      return  self.productImageArray.count
              }
            
        else {
            if self.bestSellingProductDictAr.count > 6 {
                return 6
            }
            else {
                return bestSellingProductDictAr.count
            }
        }
    }
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        if collectionView.tag == 0 {
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "SimilarProductCollectionViewCell", for: indexPath) as! SimilarProductCollectionViewCell
            cell.layer.borderColor = #colorLiteral(red: 0.8904226036, green: 0.8904226036, blue: 0.8904226036, alpha: 1)
            cell.layer.borderWidth = 1
            if self.similarProductDictAr.count != 0 {
                print(self.similarProductDictAr.count)
                let productDict = self.similarProductDictAr[indexPath.row]
                cell.lblProductWeight.text = "\(productDict["weight"] as! String) gm"
                cell.imgImage.contentMode = .scaleAspectFit
                DispatchQueue.main.async {
                    if  (productDict["image"] as? String)!.isEmpty == false {
                        let imgUrl = productDict["image"] as! String
                        let fullUrl = IMAGE_PRODUCT_URL + imgUrl
                        let url = URL(string: fullUrl)
                        cell.imgImage.sd_setImage(with: url!)
                    }
                    else {
                        cell.imgImage.image = UIImage(named:"no_image")
                    }
                    let dd = String(format: "%.2f", productDict["price"] as! Double)
                    cell.lblOrignalPrice.text = "AED \(dd)"
                    cell.lblTitle.text = productDict["name"] as? String ?? ""
                }
                cell.btnSave.tag = indexPath.row
                cell.btnSave.addTarget(self, action: #selector(addToSaveListAction), for: .touchUpInside)
                cell.cartStack.layer.cornerRadius = 5
                cell.cartStack.clipsToBounds = true
                cell.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                cell.cartStack.layer.borderWidth = 1
                cell.btnAddtoCart.tag = indexPath.row
                cell.btnAddtoCart.addTarget(self, action: #selector(addToCartbtnAction), for: .touchUpInside)
                cell.btnPlus.tag = indexPath.row
                cell.btnPlus.addTarget(self, action: #selector(btnPlusAction), for: .touchUpInside)
                cell.btnMinus.tag = indexPath.row
                cell.btnMinus.addTarget(self, action: #selector(btnMinusAction), for: .touchUpInside)
                cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                let productId = "\(productDict["id"] as! Int)"
                for index in cartDatafromDb {
                    if productId == index.product_id {
                        if let quant = index.quantity {
                            let inttype: Int = Int(quant) ?? 0
                            DispatchQueue.main.async {
                                cell.btnAddtoCart.setTitle("\(inttype)", for: .normal)
                                cell.btnAddtoCart.backgroundColor = .white
                                cell.btnAddtoCart.setTitleColor(.black, for: .normal)
                                cell.btnMinus.isHidden = false
                                cell.btnPlus.isHidden = false
                            }
                        }
                    }
                    else {
                        cell.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                        cell.btnAddtoCart.backgroundColor = .clear
                        cell.btnAddtoCart.setTitleColor(.white, for: .normal)
                        cell.btnMinus.isHidden = true
                        cell.btnPlus.isHidden = true
                    }
                }
            }
            
            return cell
        }
        else if collectionView.tag == 2 {
         let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "ImageCollectionViewCell", for: indexPath) as! ImageCollectionViewCell
            let productImagesArr = productDetailDict["product_image"]?.arrayValue
//            productImageArray = productImagesArr
            if productImagesArr?.count != 0 {
            let imageDict = productImagesArr![indexPath.row].dictionaryValue
             let url = imageDict["img"]?.stringValue
             let fullUrl = IMAGE_PRODUCT_URL + url!
            let url1 = URL(string: fullUrl)
             cell.imgProductImage.sd_setImage(with: url1!)
              cell.imgProductImage.image?.withAlignmentRectInsets(UIEdgeInsets(top: -25, left: -25, bottom: -25, right: -25))
                }
               else {
                 cell.imgProductImage.image = UIImage(named:"no_image")
               }
            return cell
        }
        else {
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "BestSellingProductCollectionViewCell", for: indexPath) as! BestSellingProductCollectionViewCell
            cell.layer.borderColor = #colorLiteral(red: 0.8904226036, green: 0.8904226036, blue: 0.8904226036, alpha: 1)
            cell.layer.borderWidth = 1
            cell.cartView.layer.cornerRadius = 5
            cell.cartView.clipsToBounds = true
            cell.cartView.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
            cell.cartView.layer.borderWidth = 1
            let productDict = self.bestSellingProductDictAr[indexPath.row]
            cell.lblProductQuantity.text = "\(productDict["weight"] as! String) gm"
            cell.productImage.contentMode = .scaleAspectFit
            DispatchQueue.main.async {
                if let imgUrl = productDict["image"] as? String {
                    let fullUrl = IMAGE_PRODUCT_URL + imgUrl
                    let url = URL(string: fullUrl)
                    cell.productImage.sd_setImage(with: url!)
                }
                else {
                    cell.productImage.image = UIImage(named:"no_image")
                }
                let dd = String(format: "%.2f", productDict["price"] as! Double)
                cell.lblProductPrice.text = "AED \(dd)"
                if let bname = productDict["brand"] {
                    cell.lblBrand.text =  bname as? String ?? ""
                }
                if let pName = productDict["name"] {
                    cell.lblProductName.text = pName as? String ?? ""
                }
            }
            cell.btnSave.tag = indexPath.row
            cell.btnSave.addTarget(self, action: #selector(addToSaveListBestAction), for: .touchUpInside)
            cell.cartView.layer.cornerRadius = 5
            cell.cartView.clipsToBounds = true
            cell.cartView.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
            cell.cartView.layer.borderWidth = 1
            cell.btnAddToCart.tag = indexPath.row
            cell.btnAddToCart.addTarget(self, action: #selector(btnAddToCartInBestbtnAction), for: .touchUpInside)
            cell.btnPlus.tag = indexPath.row
            cell.btnPlus.addTarget(self, action: #selector(btnPlusInBestAction), for: .touchUpInside)
            cell.btnMinus.tag = indexPath.row
            cell.btnMinus.addTarget(self, action: #selector(btnMinusInBestAction), for: .touchUpInside)
            cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
            let productId = "\(productDict["id"] as! Int)"
            for index in cartDatafromDb {
                if productId == index.product_id {
                    if let quant = index.quantity {
                        let inttype: Int = Int(quant) ?? 0
                        DispatchQueue.main.async {
                            cell.btnAddToCart.setTitle("\(inttype)", for: .normal)
                            cell.btnAddToCart.backgroundColor = .white
                            cell.btnAddToCart.setTitleColor(.black, for: .normal)
                            cell.btnMinus.isHidden = false
                            cell.btnPlus.isHidden = false
                        }
                    }
                }
                else {
                    cell.btnAddToCart.setTitle("ADD TO CART", for: .normal)
                    cell.btnAddToCart.backgroundColor = .clear
                    cell.btnAddToCart.setTitleColor(.white, for: .normal)
                    cell.btnMinus.isHidden = true
                    cell.btnPlus.isHidden = true
                }
            }
            return cell
        }
        
        
    }
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        
        if collectionView.tag == 0 {
            let similarDict =   self.similarArray[indexPath.row].dictionaryValue
            print(similarDict)
            let productDict = similarDict["product"]?.dictionaryValue
            let slug = productDict!["slug"]!.stringValue
            let productId = productDict!["id"]!.intValue
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
            vc.slugInDetail = slug
            vc.prId = productId
            let backButton = UIBarButtonItem()
            backButton.title = ""
            navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
            UINavigationBar.appearance().tintColor = UIColor.black
            navigationController?.pushViewController(vc, animated: true)
        }
        if collectionView.tag == 2 {
            
        }
        else if collectionView.tag == 1 {
            let similarDict =   self.bestSellingArray[indexPath.row].dictionaryValue
              print(similarDict)
              let productDict = similarDict["product"]?.dictionaryValue
              let slug = productDict!["slug"]!.stringValue
              let productId = productDict!["id"]!.intValue
              let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
              vc.slugInDetail = slug
              vc.prId = productId
              let backButton = UIBarButtonItem()
              backButton.title = ""
              navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
              UINavigationBar.appearance().tintColor = UIColor.black
              navigationController?.pushViewController(vc, animated: true)
        }
        else {
  
        }
    }
}
extension ProductDetailViewController: UICollectionViewDelegateFlowLayout{
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 0
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        if collectionView.tag == 0 {
            let numberOfItemsPerRow:CGFloat = 2
            let layout = collectionViewLayout as! UICollectionViewFlowLayout
            layout.minimumLineSpacing = 0
            layout.minimumInteritemSpacing = 0
            let itemWidth = (collectionView.bounds.width / numberOfItemsPerRow )
            print("in flowLayout")
            print(itemWidth)
            return CGSize(width: itemWidth, height: 340)
        }
        else if collectionView.tag == 2 {
            
            let numberOfItemsPerRow:CGFloat = 1
            let layout = collectionViewLayout as! UICollectionViewFlowLayout
            layout.minimumLineSpacing = 0
            layout.minimumInteritemSpacing = 0
            let itemWidth = (collectionView.bounds.width / numberOfItemsPerRow )
            print("in flowLayout")
            print(itemWidth)
            return CGSize(width: itemWidth, height: 240)
            
           // return CGSize(width: tableView.frame.size.width - 10 , height: 350)
        }
        else {
            let numberOfItemsPerRow:CGFloat = 2
            let layout = collectionViewLayout as! UICollectionViewFlowLayout
            layout.minimumLineSpacing = 0
            layout.minimumInteritemSpacing = 0
            let itemWidth = (collectionView.bounds.width / numberOfItemsPerRow )
            print("in flowLayout")
            print(itemWidth)
            return CGSize(width: itemWidth, height: 350)
        }
    }
    
    @objc func addToCartbtnAction11(_ sender: UIButton?) {
        let cell: SimilarProductTableViewCell? = (self.tableView.cellForRow(at: IndexPath.init(row: 5, section: 0)) as! SimilarProductTableViewCell)
        
        let cell1: SimilarProductCollectionViewCell? = (cell?.similarProductCollectionView.cellForItem(at: IndexPath.init(row: sender!.tag, section: 0)) as! SimilarProductCollectionViewCell)
        cell1?.btnAddtoCart.setTitle("1", for: .normal)
        cell1?.btnPlus.isHidden = false
        cell1?.btnMinus.isHidden = false
        cell1?.btnAddtoCart.backgroundColor = .white
        cell1?.btnAddtoCart.setTitleColor(.black, for: .normal)
        cell1?.btnAddtoCart.isUserInteractionEnabled = false
        cell1?.plusMinusStack.layer.cornerRadius = 5
        cell1?.plusMinusStack.clipsToBounds = true
        cell1?.plusMinusStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        cell1?.plusMinusStack.layer.borderWidth = 1
        
    }
}
extension Double
{
    func truncate(places : Int)-> Double
    {
        return Double(floor(pow(10.0, Double(places)) * self)/pow(10.0, Double(places)))
    }
}
extension Float
{
    var cleanValue: String
    {
        return self.truncatingRemainder(dividingBy: 1) == 0 ? String(format: "%.0f", self) : String(self)
    }
}
