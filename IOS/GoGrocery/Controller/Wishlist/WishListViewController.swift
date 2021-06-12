import UIKit
import SVProgressHUD
import SwiftyJSON
import FirebaseAnalytics
import SwiftyJSON
class WishListViewController: UIViewController {
    @IBOutlet weak var wishListCollectionView: UICollectionView!
    @IBOutlet weak var cartButton: UIButton!
    @IBOutlet weak var emptyListView: UIView!
    @IBOutlet weak var btnCartCount: UIButton!
    // MARK: - Variable declaration
    // MARK: -
    private let spacing:CGFloat = 1
    var productNameArr = [String]()
    var productPriceArr = [String]()
    var productImageArr = [String]()
    var productSlugArr = [String]()
    var productIdArr = [Int]()
    var cartDatafromDb = [AddcCart]()
    var cartArray = [JSON]()
    var cartDictionary = [[Int:Int]]()
    var count = Int()
    var quantity = Int()
    var productId = Int()
    var wishlistArray = [JSON]()
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var navigationType:String = ""
     var yearCheck = String()
    // MARK: - View Lifecycyle
    // MARK: -
    override func viewDidLoad() {
        super.viewDidLoad()
        emptyListView.alpha = 0
        let layout = UICollectionViewFlowLayout()
        layout.sectionInset = UIEdgeInsets(top: spacing, left: spacing, bottom: spacing, right: spacing)
        layout.minimumLineSpacing = spacing
        layout.minimumInteritemSpacing = spacing
        self.wishListCollectionView?.collectionViewLayout = layout
        apiCallToGetWishlist()
        btnCartCount.layer.cornerRadius = btnCartCount.frame.height / 2
        btnCartCount.alpha = 0
    }
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        navigationController?.setNavigationBarHidden(true, animated: true)
        ApiCallToGetCartCount()
    }
    // MARK: - Button Actions
    // MARK: -
    @IBAction func backButtonTapped(_ sender: Any) {
        if navigationType == "present" {
            dismiss(animated: true, completion: nil)
            // being presented
        }
        else {
            self.navigationController?.popViewController(animated: true)
        }
    }
    
    @IBAction func cartButtonTapped(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.pushViewController(vc, animated: true)
    }
    // MARK: - Api Calling
    // MARK: -
    func apiCallToGetWishlist() {
        let auth = UserDefaults.standard.value(forKey: "token") as! String
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        let headers:[String : Any] = ["Authorization": "Token \(auth)","WID":"\(wareHouseId)","website_id":"1" , "Content-Type": "application/json"]
     //   SVProgressHUD.show()
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "my-wish-list/", vc: self, header: headers) { (response) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].arrayValue
                self.wishlistArray = response["data"].arrayValue
                for product in data {
                    let productDict = product["product"].dictionaryValue
                    self.productNameArr.append(productDict["name"]!.stringValue)
                    self.productSlugArr.append(productDict["slug"]!.stringValue)
                    let price = String(format: "%.2f", product["new_default_price"].doubleValue)
                    self.productPriceArr.append("AED \(price)")
                    self.productIdArr.append(productDict["id"]!.intValue)
                    let productImageArray = productDict["product_image"]?.arrayValue
                    if let imageDict = productImageArray {
                        for productImage in imageDict {
                            if (productImage["img"].string)?.isEmpty == false {
                                self.productImageArr.append(productImage["img"].stringValue)
                            }
                            else {
                                self.productImageArr.append(" ")
                            }
                        }
                    } else {
                        self.productImageArr.append("")
                    }
                }
                if self.productIdArr.count > 0 {
                    self.ApiCallToViewCart()
                } else {
                    self.btnCartCount.alpha = 0
                    self.emptyListView.alpha = 1
                }
                
                print("info")
                print(self.productNameArr)
                print(self.productPriceArr)
                print(self.productImageArr)
            }
            else {
             //   SVProgressHUD.dismiss()
                self.emptyListView.alpha = 1
            }
        }
    }
    
    //    MARK:- View Cart
    func ApiCallToViewCart(){
        var auth : String?
        var deviceId : String
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
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
             //   SVProgressHUD.dismiss()
                if response["status"].intValue == 200 {
                    self.cartDictionary.removeAll()
                    let badgeCount = response["cart_count_itemwise"].intValue
                    self.btnCartCount.alpha = 1
                    self.btnCartCount.setTitle("\(badgeCount)", for: .normal)
                    self.cartButton.setImage(UIImage(named: "cart"), for: .normal)
                    let cartAr = response["data"].arrayValue
                    for product in cartAr {
                        let productDict = product["product_id"].dictionaryValue
                        let id = productDict["id"]!.intValue
                        let quantity = product["quantity"].intValue
                        self.cartDictionary.append([id:quantity])
                    }
                    self.viewDidLayoutSubviews()
                    self.wishListCollectionView.reloadData()
                }
                else {
                    self.btnCartCount.alpha = 0
                    self.cartButton.setImage(UIImage(named: "cart"), for: .normal)
                    self.wishListCollectionView.reloadData()
                    print("cart value empty")
                }
            }
        }
        else {
          //  SVProgressHUD.dismiss()
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
                    self.btnCartCount.alpha = 0
                    self.cartButton.setImage(UIImage(named: "cart"), for: .normal)
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
                    self.btnCartCount.alpha = 0
                    self.cartButton.setImage(UIImage(named: "cart"), for: .normal)
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
    
    
    //    MARK:- Button Actions
    @objc func addToCartbtnAction(sender: UIButton) {
         self.count = 0
        
        var ageString = String()
         if let ageCheckString = UserDefaults.standard.value(forKey: "Age_Check") {
             ageString = ageCheckString as! String
               yearCheck = ageString
         }
         else {
             ageString = ""
             yearCheck = ageString
         }
         
//         if ageString == "N" {
//
//         }
       //  else {
            self.count = count + 1
            var superview = sender.superview
            while let view = superview, !(view is UICollectionViewCell) {
                superview = view.superview
            }
            guard let cell = superview as? UICollectionViewCell else {
                //  print("button is not contained in a CollectionView cell")
                return
            }
            guard let indexPath = wishListCollectionView.indexPath(for: cell) else {
                // print("failed to get index path for cell containing button")
                return
            }
            guard let cell1 = superview as? ProductListingCollectionViewCell else {
                // print("rferffddvd")
                return
            }
            let tag = sender.tag
            productId = productIdArr[tag]
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
            params["warehouse_id"] = self.wareHouseId
            params["Authorization"] = "Token \(auth)"
               params["year_check"] = yearCheck
            print(params)
            postMethodQueryWithVc(apiName: "add-to-cart/", params: params, vc: self) { (response : JSON) in
                // print(response)
                if response["status"].intValue == 1 {
                    let cartDict = response["cart_data"].dictionaryValue
                    let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                    //  print(count1)
                    let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                    let count = "\(count1)"
                    let cost = "\(cost1)"
                    cell1.btnAddtoCart.setTitle("\(count)", for: .normal)
                    cell1.btnPlus.isHidden = false
                    cell1.btnMinus.isHidden = false
                    cell1.btnAddtoCart.backgroundColor = .white
                    cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                    cell1.cartStack.layer.cornerRadius = 5
                    cell1.cartStack.clipsToBounds = true
                    cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1.cartStack.layer.borderWidth = 1
                    let dict = ["cost":cost ,"product_id":"\(self.productId)","quantity":count] as [String : Any]
                    DataBaseHelper.sharedInstance.save(object: dict)
                    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                    self.count = 0
                    self.cartArray.removeAll()
                    self.ApiCallToViewCart()
                    let contentName = self.productNameArr[indexPath.row]
                      let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
                  //  let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":cost]
                    print(dictParam)
                    AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
                }
                else {
//                    cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
//                    cell1.btnPlus.isHidden = true
//                    cell1.btnMinus.isHidden = true
//                    cell1.cartStack.layer.cornerRadius = 5
//                    cell1.cartStack.clipsToBounds = true
//                    let msg = response["msg"].stringValue
//                    createalert(title: "Alert", message: msg, vc: self)
//                    self.count = 0
                    
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
                         self.count = 0
                    }
                    else {
                        let msg = response["msg"].stringValue
                        createalert(title: "Alert", message: msg, vc: self)
                      //  self.count = 0
                    }
                }
         //   }
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

        var newProductId = String()
        var newQuantity = Int()
        let coreDataindex = Int()
        var superview = sender.superview
        while let view = superview, !(view is UICollectionViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UICollectionViewCell else {
            // print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = wishListCollectionView.indexPath(for: cell) else {
            // print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? ProductListingCollectionViewCell else {
            //print("rferffddvd")
            return
        }
        // We've got the index path for the cell that contains the button, now do something with it.
        let tag = sender.tag
        let productId = "\(productIdArr[tag])"
        newProductId = productId
        newQuantity = getCartQuantity(id: productIdArr[tag]) + 1
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
        params["warehouse_id"] = self.wareHouseId
            params["year_check"] = yearCheck
        postMethodQueryWithVc(apiName: "add-to-cart/", params: params, vc: self) { (response : JSON) in
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
                cell1.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
                cell1.btnPlus.isHidden = false
                cell1.btnMinus.isHidden = false
                cell1.btnAddtoCart.backgroundColor = .white
                cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                cell1.cartStack.layer.cornerRadius = 5
                cell1.cartStack.clipsToBounds = true
                cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                cell1.cartStack.layer.borderWidth = 1
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                self.cartArray.removeAll()
                self.ApiCallToViewCart()
                let contentName = self.productNameArr[indexPath.row]
                  let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName]
               // let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName,"Currency":"AED","ValueToSum":cost]
                print(dictParam)
                AddCart(dictParam: dictParam)
                logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName, currency: "AED", valueToSum: cost)
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
        let coreDataindex = Int()
        let tempCost = String()
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        var superview = sender.superview
        while let view = superview, !(view is UICollectionViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UICollectionViewCell else {
            //    print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = wishListCollectionView.indexPath(for: cell) else {
            //    print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? ProductListingCollectionViewCell else {
            //    print("rferffddvd")
            return
        }
        // We've got the index path for the cell that contains the button, now do something with it.
        let tag = sender.tag
        let productId = "\(productIdArr[tag])"
        newProductId = productId
        newQuantity = getCartQuantity(id: productIdArr[tag]) - 1
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
        params["warehouse_id"] = self.wareHouseId
        params["year_check"] = yearCheck
        postMethodQueryWithVc(apiName: "add-to-cart/", params: params, vc: self) { (response : JSON) in
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                cell1.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
                cell1.btnPlus.isHidden = false
                cell1.btnMinus.isHidden = false
                if count1 == 0 {
                    DataBaseHelper.sharedInstance.delete(index: coreDataindex)
                    cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                    cell1.btnPlus.isHidden = true
                    cell1.btnMinus.isHidden = true
                    cell1.lblOrignalPrice.text = "AED \(tempCost)"
                    cell1.btnAddtoCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
                    cell1.btnAddtoCart.setTitleColor(.white, for: .normal)
                    cell1.cartStack.layer.cornerRadius = 5
                    cell1.cartStack.clipsToBounds = true
                    cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1.cartStack.layer.borderWidth = 1
                }
                else {
                    DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                }
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                self.cartArray.removeAll()
                self.ApiCallToViewCart()
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
    
    @objc func deleteWishListItem(sender: UIButton) {
        let tag = sender.tag
        let productId = "\(productIdArr[tag])"
        var params = [String:Any]()
        params["product_id"] = productId
        postMethodQuery2(apiName: "delete-wishlist/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.productNameArr.remove(at: tag)
                self.productPriceArr.remove(at: tag)
                self.productImageArr.remove(at: tag)
                self.productSlugArr.remove(at: tag)
                self.productIdArr.remove(at: tag)
                self.wishListCollectionView.reloadData()
                if self.productIdArr.count == 0 {
                    self.emptyListView.alpha = 1
                }
            }
            else {
                let msg = response["msg"].stringValue
                createalert(title: "Alert", message: msg, vc: self)
                if self.productIdArr.count == 0 {
                    self.emptyListView.alpha = 1
                }
            }
        }
    }
    
    func getCartQuantity(id:Int)->Int {
        var cartQuantity = 0
        for cartDict in self.cartDictionary {
            if cartDict.index(forKey: id) != nil {
                cartQuantity = cartDict[id]!
            }
        }
        return cartQuantity
    }
}


//MARK:- CollectionView Delegate
extension WishListViewController : UICollectionViewDelegate, UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return self.productIdArr.count
    }
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "WishListCollectionViewCell", for: indexPath) as! ProductListingCollectionViewCell
        cell.lblProductWeight.text = ""
        let wishlistDict = self.wishlistArray[indexPath.row].dictionaryValue
        let productDict = wishlistDict["product"]!.dictionaryValue
        let url = IMAGE_PRODUCT_URL + "\(self.productImageArr[indexPath.row])"
          let fullurl = URL(string: url)
        cell.imgImage.setImageWith(fullurl!, placeholderImage: UIImage(named: "no_image"))
        cell.lblOrignalPrice.text = self.productPriceArr[indexPath.row]
        cell.lblTitle.text = self.productNameArr[indexPath.row]
        cell.btnSave.tag = indexPath.row
        cell.btnSave.addTarget(self, action: #selector(deleteWishListItem), for: .touchUpInside)
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
        let cartQuantity = getCartQuantity(id: self.productIdArr[indexPath.row])
        if cartQuantity > 0 {
            cell.btnAddtoCart.setTitle("\(cartQuantity)", for: .normal)
            cell.btnAddtoCart.backgroundColor = .white
            cell.btnAddtoCart.setTitleColor(.black, for: .normal)
            cell.btnMinus.isHidden = false
            cell.btnPlus.isHidden = false
        } else {
            cell.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
            cell.btnAddtoCart.backgroundColor = .clear
            cell.btnAddtoCart.setTitleColor(.white, for: .normal)
            cell.btnMinus.isHidden = true
            cell.btnPlus.isHidden = true
        }
        
        return cell
    }
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
        vc.slugInDetail = self.productSlugArr[indexPath.row]
        vc.prId = self.productIdArr[indexPath.row]
        self.navigationController?.pushViewController(vc, animated: true)
    }
}
extension WishListViewController: UICollectionViewDelegateFlowLayout{
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 1
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let numberOfItemsPerRow:CGFloat = 2
        let spacingBetweenCells:CGFloat = 1
        
        let totalSpacing = (2 * self.spacing) + ((numberOfItemsPerRow - 1) * spacingBetweenCells) //Amount of total spacing in a row
        
        if let collection = self.wishListCollectionView{
            let width = (collection.bounds.width - totalSpacing)/numberOfItemsPerRow
            return CGSize(width: width, height: 310)
        }
        else{
            return CGSize(width: 0, height: 0)
        }
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 1
    }
}


