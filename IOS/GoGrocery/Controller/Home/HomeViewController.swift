
import UIKit
import SwiftyJSON
import ImageSlideshow
import FirebaseAnalytics
import Alamofire
class HomeViewController: UIViewController,CategorySelectDelegate ,BannerSelectDelegate ,BrandSelectDelegate , BestSellingSelectDelegate{
    // MARK: - Outlet declaration
    // MARK: -
    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var btnSearch: UIButton!
    @IBOutlet weak var btnLocation: UIButton!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var lblWarehouseName: UILabel!
    @IBOutlet weak var imgLogo: UIImageView!
    @IBOutlet weak var btnCart: UIButton!
    @IBOutlet weak var btnCartCount: UIButton!
    
    @IBOutlet weak var menuTableView : UITableView!
    @IBOutlet weak var childTitleLabel: UILabel!
    @IBOutlet weak var backViewHeight: NSLayoutConstraint!
    @IBOutlet weak var userInfoView: UIView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var phoneLabel: UILabel!
    @IBOutlet weak var menuTapView: UIView!
    
    @IBOutlet weak var menuContainerView: UIView!
    
    @IBOutlet weak var menuView: UIView!
    @IBOutlet weak var menuContainerLeading: NSLayoutConstraint!
    
    @IBOutlet weak var menuContainerTrailing: NSLayoutConstraint!
    // MARK: - Variable declaration
    // MARK: -
    
    
    var menuList = MenuList(status: 0, menuBar: nil)
    var menuChild = [[Child(id: nil, parentID: nil, name: nil, childDescription: nil, image: nil, thumbImage: nil, bannerImage: nil, pageTitle: nil, metaDescription: nil, metaKeywords: nil, categoryURL: nil, slug: nil, websiteID: nil, isEbayStoreCategory: nil,  displayMobileApp: nil, showNavigation: nil, grandParentID: nil, child: nil)]]
    var level = 0
    var lastTitle = ""
    var titleArray = [String]()
    let subMenu = ["My Orders","My Cart","My WishList","My Account","Contact Us","About Us" ,"Our Vision & Purpose" ,"Quality Standards" ,"Privacy Policy" ,"Terms & Conditions","Login"]
    let subMenuImage = ["my_orders","cart","wishlist_grey","avatar","call","about","vision","standard","privacy","terms","logout"]
    var currentScrollPosition:CGFloat = 0
    var scrollPositionArray = [CGFloat]()
    
    
    var commonCell = UITableViewCell()
    let transiton = SlideInTransition()
    var mainMenuNameArray = NSMutableArray()
    var mainMenuChildArray = NSMutableArray()
    var mainMenuArray = NSArray()
    var cmsMenuArray = NSArray()
    var subMenuArray = NSArray()
    var menuVC = SidemenuController()
    var userDict = [String : JSON]()
    var homeArray = [String : JSON]()
    var carouselArray = [JSON]()
    var categoryArray = [JSON]()
    var dealsArray = [JSON]()
    var bannnerArray = [JSON]()
    var bestSellArray = [JSON]()
    var brandArray = [JSON]()
    var sdWebImageSource = [SDWebImageSource]()
    var wareHouseId = Int()
    var wareHouseName = String()
    var productID = Int()
    var quantity = Int()
    var cartDatafromDb = [AddcCart]()
    var cartNotiDict = [String:Any]()
    var sender = Int()
    var saveProductId = Int()
    var cartArray = [JSON]()
    var slugFromHome = String()
    var cellCategoryTemp = [JSON]()
    var badgeCount = Int()
    var catArray = [JSON]()
    var frstTimePushFromSideMenuToProductListing:Bool = false
    // MARK: - View lifecycle
    // MARK: -
    
    override func viewDidLoad() {
        super.viewDidLoad()
        

        // ApiCallToGetMenuList()
        btnCartCount.layer.cornerRadius = btnCartCount.frame.height/2
        print(slugFromHome)
        sdWebImageSource.removeAll()
        wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as? Int ?? 0
        wareHouseName = UserDefaults.standard.value(forKey: "WareHouseName") as? String ?? ""
        self.lblWarehouseName.text = "\(wareHouseName)"
        navigatSideMenuSelection()
        self.ApiCallToGetHomeData()
        self.callMenuListWebservice()
        
        let mytapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(menuContainerTapAction))
        mytapGestureRecognizer.numberOfTapsRequired = 1
        self.menuTapView.addGestureRecognizer(mytapGestureRecognizer)
        menuTableView.separatorStyle = .singleLine
     //   NotificationCenter.default.addObserver(self, selector: #selector(self.UpdateMenu), name: Notification.Name("MenuUpdate"), object: nil)
    }
   /* @objc func UpdateMenu() {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            if UserDefaults.standard.value(forKey: "is-login") as! Bool == true {
                self.ApiCallTogetUserDetails()
               // self.callMenuListWebservice()
        }
    }
    }
 */
    
    override func didReceiveMemoryWarning() {
        print("")
    }
    override func viewWillAppear(_ animated: Bool) {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                if UserDefaults.standard.value(forKey: "is-login") as! Bool == true {
                    self.ApiCallTogetUserDetails()
                   // self.callMenuListWebservice()
            }
        }
        hideSideMenu()
        CheckLogin()
      //  ApiCallToGetCartCount()
        self.navigationController?.setNavigationBarHidden(true, animated: true)
        self.navigationView.addShadow1()
        UserDefaults.standard.removeObject(forKey: "category_Array")
        UserDefaults.standard.removeObject(forKey: "brand_Array")
        UserDefaults.standard.synchronize()
        
        NotificationCenter.default.addObserver(self, selector: #selector(HomeViewController.updateCart(notification:)), name: NSNotification.Name(rawValue: "CartUpdate"), object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(HomeViewController.showAlertonfailure(notification:)), name: NSNotification.Name(rawValue: "AddCartfailure"), object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(self.transferFromSideMenuToProductListing), name: Notification.Name("TransferSlugSideMenuToProductListing"), object: nil)
    }
    
    @objc func menuContainerTapAction(recognizer: UITapGestureRecognizer) {
        hideSideMenu()
    }
    @objc func menuViewTapAction(recognizer: UITapGestureRecognizer) {
        print("do nothing")
    }
    
    func hideSideMenu() {
        level = 0
        self.titleArray.removeAll()
        self.menuChild.removeAll()
        //  self.menuContainerView.backgroundColor = .clear
        menuContainerLeading.constant = 0 - UIScreen.main.bounds.size.width
        menuContainerTrailing.constant = UIScreen.main.bounds.size.width
        UIView.animate(withDuration: 0.3, animations: { () -> Void in
            self.tabBarController?.tabBar.isHidden = false
            self.view.layoutIfNeeded()
        }, completion: nil)
    }
    
    func revealSideMenu() {
        addDataToMenuList()
        self.menuTableView.setContentOffset(CGPoint.zero, animated:true)
        self.menuContainerView.backgroundColor = .clear
        menuContainerLeading.constant = 0
        menuContainerTrailing.constant = 0
        UIView.animate(withDuration: 0.3, animations: { () -> Void in
            self.tabBarController?.tabBar.isHidden = true
            self.view.layoutIfNeeded()
        }, completion: { (Bool) in
            UIView.animate(withDuration: 0.1) {
                self.menuContainerView.backgroundColor = UIColor.black.withAlphaComponent(0.15)
            }
        })
    }
    
    func addDataToMenuList() {
        if level == 0 {
            backViewHeight.constant = 0
        }
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            ApiCallTogetUserDetails()
            //        let name = UserDefaults.standard.value(forKey: STRING_CONSTANT.USER_NAME) as! String
            //        let phone = UserDefaults.standard.value(forKey: STRING_CONSTANT.USER_PHONE) as! String
            //        self.nameLabel.text = name
            //        self.phoneLabel.text = phone
        }
        else {
            self.userInfoView.alpha = 0
        }
       // print(UserDefaults.standard.value(forKey: "menudata"))
        if UserDefaults.standard.value(forKey: "menudata") != nil {
            let menuData = UserDefaults.standard.value(forKey: "menudata") as! Data
            do{
                let r = try JSONDecoder().decode(MenuList.self, from: menuData)
                self.menuList = r
                self.menuTableView.dataSource = self
                self.menuTableView.delegate = self
                self.menuTableView.reloadData()
                self.tableView.reloadData()
            }catch{
                print("catch error \(error)")
            }
        }
    }
    
    func ApiCallTogetUserDetails() {
        getMethodWithAuthorizationReturnJson(apiName: "my-profile/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                self.nameLabel.text = "\(data["first_name"]!.string ?? "") \(data["last_name"]!.string ?? "")"
              //  UserDefaults.standard.setValue("\(self.nameLabel.text)", forKey: "username")
              //  UserDefaults.standard.synchronize()
                if let mob = data["phone"]?.string {
                    self.phoneLabel.text = data["phone"]!.string ?? ""
                    self.phoneLabel.isHidden = false
                }
                self.userInfoView.alpha = 1
            }
        }
    }
    @IBAction func btnProfileAction(_ sender: Any) {
        hideSideMenu()
        //tabBarController!.selectedIndex = 3
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                hideSideMenu()
                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let viewController = storyboard.instantiateViewController(withIdentifier: "ProfileViewController") as! ProfileViewController
                let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                navigationController.pushViewController(viewController, animated: true)
            }
            else {
                hideSideMenu()
                let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                navigationController.pushViewController(viewController, animated: true)
                
            }
        }
        else {
            hideSideMenu()
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
            navigationController.pushViewController(viewController, animated: true)
        }
        
    }
    
    @IBAction func subMenuBackButtonClickAction(_ sender: UIButton) {
        if level <= 1 {
            self.backViewHeight.constant = 0
            level = 0
            self.menuChild.remove(at: self.menuChild.count-1)
            self.titleArray.remove(at: self.titleArray.count-1)
            DispatchQueue.main.async {
                let offset = CGPoint.init(x: 0, y: self.scrollPositionArray[self.scrollPositionArray.count-1])
                self.menuTableView.setContentOffset(offset, animated: false)
                self.scrollPositionArray.remove(at: self.scrollPositionArray.count-1)
            }
            
        } else {
            self.titleArray.remove(at: self.titleArray.count-1)
            self.childTitleLabel.text = self.titleArray[self.titleArray.count-1]
            level = level - 1
            self.menuChild.remove(at: self.menuChild.count-1)
            DispatchQueue.main.async {
                let offset = CGPoint.init(x: 0, y: self.scrollPositionArray[self.scrollPositionArray.count-1])
                self.menuTableView.setContentOffset(offset, animated: false)
                self.scrollPositionArray.remove(at: self.scrollPositionArray.count-1)
            }
            
        }
        
        self.menuTableView.reloadData()
        //self.listTableView.setContentOffset(CGPoint.zero, animated:true)
        //self.dismiss(animated: true, completion: nil)
    }
    
    // MARK: - Button Actions
    // MARK: -
    
    @IBAction func btnCallAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ContactUsViewController") as! ContactUsViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    @IBAction func btnCartAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnLocationAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
        vc.withinApp = false
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnSearchAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "SearchViewController") as! SearchViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func navigatSideMenuSelection() {
        menuVC = self.storyboard!.instantiateViewController(withIdentifier: "MENU") as! SidemenuController
        menuVC.menuSelection = { selection in
        }
    }
    @objc func transferFromSideMenuToProductListing (notification: NSNotification) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
        let dict = notification.userInfo as! [String:Any]
        print(dict)
        self.slugFromHome = dict["slug"] as! String
        let title = dict["title"] as! String
        vc.productTitle = title
        vc.slugInListing = self.slugFromHome
        vc.sideMenuBool = true
        NotificationCenter.default.removeObserver(self)
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @objc func filterTapped() {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    func CheckLogin() {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            DataBaseHelper.sharedInstance.deleteAllRecords()
            ApiCallTogetUserDetails()
            ApiCallToGetCartCount()
            // ApiCallToViewCart()
        }
        else {
            ApiCallToGetCartCount()
            // ApiCallToViewCart()
            DataBaseHelper.sharedInstance.deleteAllRecords()
        }
    }
    
    @objc func notiSaveBtn(_ notification:Notification) {
        
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            if UserDefaults.standard.value(forKey: "is-login") as! Bool == true {
                //  print(notification.userInfo)
                let userDict = notification.userInfo
                self.saveProductId = userDict!["product_id"] as! Int
                let name = userDict!["name"] as! String
                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "SaveListViewController") as! SaveListViewController
                vc.productIdInSave = self.saveProductId
                vc.nameInsave = name
                self.navigationController?.pushViewController(vc, animated: true)
            }
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
            self.navigationController?.pushViewController(vc, animated: true)
        }
    }
    //    MARK:- Custom delegate
    
    func filterTypeSelected(id: Int, slug: String, category_type: String ,type : String) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
        print(slug)
        vc.productTitle = category_type
        vc.slugInListing = slug
        vc.type = type
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        let contentName  = category_type
        let dictParam :[String:Any] = ["Content_ID":"\(id)","Content_Type":contentName]
        print(dictParam)
        self.VisitCategory(dictParam: dictParam)
        logViewContentEvent(contentType: contentName, contentData: "N/A", contentId: "\(id)", currency: "AED", price: 00.00)
        self.navigationController?.pushViewController(vc, animated: true)
    }
    func BannerTypeSelected(id: Int, slug: String, category_type: String ,type : String) {
        
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
        print(slug)
        vc.slugInListing = slug
        vc.productTitle = category_type
        let contentName  = category_type
        let dictParam :[String:Any] = ["Content_ID":"\(id)","Content_Type":contentName]
        print(dictParam)
        self.VisitCategory(dictParam: dictParam)
        logViewContentEvent(contentType: contentName, contentData: "N/A", contentId: "\(id)", currency: "AED", price: 00.00)
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func BrandTypeSelected(id: Int, slug: String, category_type: String, type: String, brandSelect: Bool) {
        print(slug)
        print(category_type)
        print(type)
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
        vc.productTitle = category_type
        vc.slugInListing = slug
        vc.type = type
        vc.brandBool = brandSelect
        vc.isBrandSelect = true
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        let contentName  = category_type
        let dictParam :[String:Any] = ["Content_ID":"\(id)","Content_Type":contentName]
        print(dictParam)
        self.VisitCategory(dictParam: dictParam)
        logViewContentEvent(contentType: contentName, contentData: "N/A", contentId: "\(id)", currency: "AED", price: 00.00)
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func BestSellingTypeSelected(id: Int, slug: String, category_type: String, type: String) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
        vc.slugInDetail = slug
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        let contentName  = category_type
        let dictParam :[String:Any] = ["Content_ID":"\(id)","Content_Type":contentName]
        print(dictParam)
        self.VisitCategory(dictParam: dictParam)
        logViewContentEvent(contentType: contentName, contentData: "N/A", contentId: "\(id)", currency: "AED", price: 00.00)
        self.navigationController?.pushViewController(vc, animated: true)
    }
    @IBAction func btnEditAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func didTapMenu(_ sender: UIButton) {
        //
        //        menuVC.userDict1 = userDict
        //        menuVC.revealSideMenu()
        revealSideMenu()
    }
    
    // MARK: - Api Calling
    // MARK: -
    
    func callMenuListWebservice() {
        //var dictParam = [AnyHashable: Any]()
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        let dictParam: [String : Any] = ["website_id" : 1 ,
                                         "lang_code" : "en",
                                         "warehouse_id": wareHouseId]
        let url = baseUrl + "menu_bar/"
        // callMenuWebService(url: url, imageData: nil, parameters: dictParam)
        callMenuWebService(url: url, imageData: nil, parameters: dictParam)
        
    }
    
    func ApiCallToGetHomeData() {
        var params = [String:Any]()
        params["company_website_id"] = 1
        params["lang"] = "en"
        params["template_id"] = 1
        params["page_id"] = 9
        params["start_limit"] = 0
        params["end_limit"] = 70
        params["warehouse_id"] = wareHouseId
        print(params)
        postMethodSocialSignIn(apiName: "home-cms/", params: params, vc: self) { (response:JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                self.homeArray = response["data"].dictionaryValue
                let dataDict = response["data"].dictionaryValue
                if dataDict["carousel"]?.arrayValue.count != 0 {
                    self.carouselArray = dataDict["carousel"]!.arrayValue
                    for i in 0...self.carouselArray.count - 1 {
                        let carsouselDict = self.carouselArray[i].dictionaryValue
                        let carouselUrl = carsouselDict["primary_image_name"]?.stringValue
                        let url = IMAGE_SLIDER_URL + carouselUrl!
                        self.sdWebImageSource.append(SDWebImageSource(urlString: url)!)
                    }
                }
                var catNameArr = [String]()
                if dataDict["Shop_By_Category"]?.arrayValue.count != 0 {
                    let cArray = dataDict["Shop_By_Category"]?.arrayValue
                    for index in cArray! {
                        if index["image"].string!.isEmpty != true {
                            self.catArray.append(index)
                            catNameArr.append(index["name"].string ?? "")
                        }
                    }
                    UserDefaults.standard.set(catNameArr, forKey: "homeCategoryName")
                    UserDefaults.standard.synchronize()
                }
                if dataDict["category_banner"]?.arrayValue.count != 0 {
                    self.bannnerArray = dataDict["category_banner"]!.arrayValue
                    //                        print(self.bannnerArray.count)
                }
                if dataDict["shop_by_brand"]?.arrayValue.count != 0 {
                    let brandTemp = dataDict["shop_by_brand"]!.arrayValue
                    for index in brandTemp {
                        //                            print(index)
                        if index["brand_logo"].string != nil {
                            self.brandArray.append(index)
                        }
                    }
                }
                print(self.brandArray.count)
                self.tableView.dataSource = self
                self.tableView.delegate = self
                self.tableView.reloadData()
            }
        }
    }
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
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    for index in self.cartArray {
                        let  cost = "\(index["new_default_price_unit"].doubleValue)"
                        let productDict = index["product_id"].dictionaryValue
                        let newQuantity = "\(index["quantity"].intValue)"
                        let productId = "\(productDict["id"]!.intValue)"
                        let dict = ["cost":cost ,"product_id":"\(productId)","quantity":newQuantity] as [String : Any]
                        DataBaseHelper.sharedInstance.save(object: dict)
                    }
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
                if response["status"].intValue == 200 {
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    for index in self.cartArray {
                        let  cost = "\(index["new_default_price_unit"].doubleValue)"
                        let productDict = index["product_id"].dictionaryValue
                        let newQuantity = "\(index["quantity"].intValue)"
                        let productId = "\(productDict["id"]!.intValue)"
                        let dict = ["cost":cost ,"product_id":"\(productId)","quantity":newQuantity] as [String : Any]
                        DataBaseHelper.sharedInstance.save(object: dict)
                    }
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
    
    func ApiCallToLogout() {
        
         //  let api = "http://15.185.126.44:8062/api/picker-logout/"
            let api = "http://gogrocery.ae:81/api/picker-logout/"
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
                   let alertController = UIAlertController(title: "Alert", message: "Something went wrong. Please try again", preferredStyle:.alert)

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
    
    //    MARK:- Handle Observing Notifications
    @objc func showAlertonfailure(notification: Notification) {
        let msgDict = notification.userInfo
        let msg = msgDict!["msg"] as! String
        createalert(title: "Alert", message: msg, vc: self)
    }
    @objc func updateCart(notification: Notification) {
        ApiCallToGetCartCount()
    }
    //MARK:- Events
    //MARK:-
    
    func VisitCategory(dictParam : [String:Any]) {
        Analytics.logEvent("visit_category", parameters: dictParam)
    }
}
//MARK:- Extensions
//MARK:-
extension HomeViewController: UIViewControllerTransitioningDelegate {
    func animationController(forPresented presented: UIViewController, presenting: UIViewController, source: UIViewController) -> UIViewControllerAnimatedTransitioning? {
        transiton.isPresenting = true
        return transiton
    }
    
    func animationController(forDismissed dismissed: UIViewController) -> UIViewControllerAnimatedTransitioning? {
        transiton.isPresenting = false
        return transiton
    }
}
extension HomeViewController: ImageSlideshowDelegate {
    func imageSlideshow(_ imageSlideshow: ImageSlideshow, didChangeCurrentPageTo page: Int) {
    }
}
extension HomeViewController : UITableViewDelegate, UITableViewDataSource {
    func numberOfSections(in tableView: UITableView) -> Int {
        if tableView == menuTableView {
            return 2
        }
        else {
            return 1
        }
    }
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if tableView == menuTableView {
            if section == 0 {
                print("level  \(level)")
                if level == 0 {
                    return self.menuList.menuBar?.count ?? 0
                } else {
                    let mChild = self.menuChild[menuChild.count-1]
                    return mChild.count
                }
                
            }else if section == 1{
                return self.subMenu.count
            }else{
                return 0
            }
        }
        else {
            return homeArray.count
        }
        // return homeArray.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        print(indexPath.row)
        if tableView == menuTableView {
            if indexPath.section == 0 {
                guard let cell = self.menuTableView.dequeueReusableCell(withIdentifier: "sideMenuCell", for: indexPath)
                    as? sideMenuCell else { fatalError("cell return null")}
                var name = ""
                if level == 0 {
                    name = self.menuList.menuBar?[indexPath.row].name ?? ""
                }else {
                    let mChild = self.menuChild[menuChild.count-1]
                    name = mChild[indexPath.row].name ?? ""
                }
                
                cell.menuTitleLabel.text = name
                return cell
            }
            else if indexPath.section == 1 {
                guard let cell = self.menuTableView.dequeueReusableCell(withIdentifier: "sideSubMenuCell", for: indexPath)
                    as? sideMenuCell else { fatalError("cell return null")}
                cell.menuIcon.image = UIImage(named: self.subMenuImage[indexPath.row])
                if indexPath.row == self.subMenu.count - 1 {
                    if UserDefaults.standard.value(forKey: "is-login") != nil {
                        cell.menuTitleLabel.text = "Logout"
                    }
                    else {
                        cell.menuTitleLabel.text = "Login"
                    }
                } else {
                    cell.menuTitleLabel.text = self.subMenu[indexPath.row]
                }
                
                return cell
            }else{
                return UITableViewCell()
            }
        }
        else {
            if indexPath.row == 0 {
                let slideCell = tableView.dequeueReusableCell(withIdentifier: "SlideTableViewCell", for: indexPath) as! SlideTableViewCell
                slideCell.slideshow.slideshowInterval = 5.0
                slideCell.slideshow.pageIndicatorPosition = .init(horizontal: .center, vertical: .bottom)
                slideCell.slideshow.contentScaleMode = UIView.ContentMode.scaleToFill
                let pageControl = UIPageControl()
                pageControl.currentPageIndicatorTintColor = UIColor.lightGray
                pageControl.pageIndicatorTintColor = UIColor.black
                slideCell.slideshow.pageIndicator = pageControl
                slideCell.slideshow.activityIndicator = DefaultActivityIndicator()
                slideCell.slideshow.delegate = self
                slideCell.slideshow.setImageInputs(sdWebImageSource as [InputSource])
                slideCell.cellCaraouselArray = self.carouselArray
                commonCell = slideCell
            }
            else if indexPath.row == 1 {
                
                let categoryCell = tableView.dequeueReusableCell(withIdentifier: "CategoryTableViewCell", for: indexPath) as! CategoryTableViewCell
                categoryCell.cellCategoryArray = self.catArray
                categoryCell.delegate = self
                commonCell = categoryCell
            }
            else if indexPath.row == 2 {
                let bannnerCell = tableView.dequeueReusableCell(withIdentifier: "BannerTableViewCell", for: indexPath) as! BannerTableViewCell
                bannnerCell.cellBannerArray = self.bannnerArray
                bannnerCell.bannerdelegate = self
                commonCell = bannnerCell
            }
            else if indexPath.row == 3 {
                let bestSellCell = tableView.dequeueReusableCell(withIdentifier: "BestSellingTableViewCell", for: indexPath) as! BestSellingTableViewCell
                bestSellCell.cellBestSellingArray = self.bestSellArray
                bestSellCell.delegate = self
                commonCell = bestSellCell
            }
            else if indexPath.row == 4 {
                let dealsCell = tableView.dequeueReusableCell(withIdentifier: "DealsOfTheDayTableViewCell", for: indexPath) as! DealsOfTheDayTableViewCell
                dealsCell.cellDealsArray = self.dealsArray
                commonCell = dealsCell
            }
            else {
                let brandCell = tableView.dequeueReusableCell(withIdentifier: "BrandTableViewCell", for: indexPath) as! BrandTableViewCell
                brandCell.cellBrandCell = self.brandArray
                brandCell.branddelegate = self
                commonCell = brandCell
            }
            return commonCell
        }
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        if tableView == menuTableView {
            if indexPath.section == 0 {
                return 40
            } else {
                return 50
            }
        }
        else {
            if indexPath.row == 0 {
                if  self.carouselArray.count != 0 {
                    return 220
                }
                else {
                    return 0
                }
                
            }
            else if indexPath.row == 1 {
                return 210
            }
            else if indexPath.row == 2 {
                var height: CGFloat
                if bannnerArray.count != 0 {
                    height = CGFloat(170 * bannnerArray.count) + CGFloat(10 * bannnerArray.count)
                    // height = CGFloat(130 * bannnerArray.count + 1)
                    print(height)
                }
                else {
                    height = 0
                }
                return height
            }
            else if indexPath.row == 3 {
                //            var height : CGFloat
                //            if bestSellArray.count != 0 {
                //                height = 342
                //            }
                //            else {
                //                height = 0
                //            }
                return 0
            }
            else if indexPath.row == 4 {
                //            var height: CGFloat
                //            if dealsArray.count != 0 {
                //                height = 500
                //            }
                //            else {
                //                height = 0
                //            }
                return 0
            }
            else if indexPath.row == 5 {
                var height: CGFloat
                if brandArray.count != 0 {
                    height = 150
                    //return 130
                }
                else {
                    height = 0
                }
                return height
            }
            else {
                return 0
            }
        }
        
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if tableView == menuTableView {
            if indexPath.section == 0{
                self.backViewHeight.constant = 40
                if level == 0 {
                    if self.menuList.menuBar?[indexPath.row].child?.count ?? 0 > 0 {
                        self.titleArray.append(self.menuList.menuBar?[indexPath.row].name ?? "")
                        self.childTitleLabel.text = self.menuList.menuBar?[indexPath.row].name
                        self.menuChild.append((self.menuList.menuBar?[indexPath.row].child)!)
                        level = level + 1
                        let position = menuTableView.contentOffset.y
                        self.scrollPositionArray.append(position)
                        self.menuTableView.reloadData()
                        let topIndex = IndexPath(row: 0, section: 0)
                        menuTableView.scrollToRow(at: topIndex, at: .top, animated: true)
                        //self.listTableView.setContentOffset(CGPoint.zero, animated:true)
                    } else {
                        let storyBoard = UIStoryboard(name: "Home", bundle: nil)
                        let vc = storyBoard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
                        vc.slugInListing = self.menuList.menuBar?[indexPath.row].slug ?? ""
                        vc.productTitle = self.menuList.menuBar?[indexPath.row].name ?? ""
                        self.navigationController?.show(vc, sender: self)
                    }
                    
                } else {
                    let mChild = self.menuChild[menuChild.count-1]
                    //                        if mChild[indexPath.row].child?.count ?? 0 > 0 {
                    //                            self.titleArray.append(mChild[indexPath.row].name ?? "")
                    //                            self.childTitleLabel.text = mChild[indexPath.row].name
                    //                            self.menuChild.append(mChild[indexPath.row].child!)
                    //                            let position = menuTableView.contentOffset.y
                    //                            self.scrollPositionArray.append(position)
                    //                            level = level + 1
                    //                            self.menuTableView.reloadData()
                    //                            let topIndex = IndexPath(row: 0, section: 0)
                    //                            menuTableView.scrollToRow(at: topIndex, at: .top, animated: true)
                    //                            //self.listTableView.setContentOffset(CGPoint.zero, animated:true)
                    //                        } else {
                    let storyBoard = UIStoryboard(name: "Home", bundle: nil)
                    let vc = storyBoard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
                    vc.slugInListing = mChild[indexPath.row].slug ?? ""
                    vc.productTitle = mChild[indexPath.row].name ?? ""
                    self.navigationController?.show(vc, sender: self)
                    // }
                }
                //            if indexPath.row == 1{
                //                self.pushToNextViewControllerWithNavigationController(storyboardName: Constants.StoryboardsID.home.rawValue, viewcontroller: ProductListViewController.className, navcontroller: self.navigationController!)
                //            }
            }
            else if indexPath.section == 1 {
                if indexPath.row == 0 {
                    if UserDefaults.standard.value(forKey: "is-login") != nil {
                        if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                            hideSideMenu()
                            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                            let viewController = storyboard.instantiateViewController(withIdentifier: "MyOrdersViewController") as! MyOrdersViewController
                            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                            navigationController.pushViewController(viewController, animated: true)
                        }
                        else {
                            hideSideMenu()
                            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                            navigationController.pushViewController(viewController, animated: true)
                        }
                    }
                    else {
                        hideSideMenu()
                        let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                        let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                        navigationController.pushViewController(viewController, animated: true)
                    }
                }
                else if indexPath.row == 1 {
                    //  hideSideMenu()
                    let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                    
                }
                else if indexPath.row == 2 {
                    if UserDefaults.standard.value(forKey: "is-login") != nil {
                        if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                            
                            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                            let viewController = storyboard.instantiateViewController(withIdentifier: "WishListViewController") as! WishListViewController
                            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                            navigationController.pushViewController(viewController, animated: true)
                        }
                        else {
                            
                            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                            navigationController.pushViewController(viewController, animated: true)
                        }
                    }
                    else {
                        
                        let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                        let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                        navigationController.pushViewController(viewController, animated: true)
                    }
                }
                else if indexPath.row == 3 {
                    if UserDefaults.standard.value(forKey: "is-login") != nil {
                        if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                            hideSideMenu()
                            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                            let viewController = storyboard.instantiateViewController(withIdentifier: "ProfileViewController") as! ProfileViewController
                            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                            navigationController.pushViewController(viewController, animated: true)
                        }
                        else {
                            hideSideMenu()
                            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                            let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                            navigationController.pushViewController(viewController, animated: true)
                            
                        }
                    }
                    else {
                        hideSideMenu()
                        let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                        let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                        navigationController.pushViewController(viewController, animated: true)
                    }
                    
                }
                else if indexPath.row == 4 {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "ContactUsViewController") as! ContactUsViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                    
                }
                else if indexPath.row == 5 {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "AboutUsViewController") as! AboutUsViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                    
                }
                    
                else if indexPath.row == 6 {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "OurVisionAndPurposeViewController") as! OurVisionAndPurposeViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                   navigationController.pushViewController(viewController, animated: true)
                    
                }
                    
                else if indexPath.row == 7 {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "QualityStandardViewController") as! QualityStandardViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                    
                }
                else if indexPath.row == 8 {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "PrivacyPolicyViewController") as! PrivacyPolicyViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                    
                }
                else if indexPath.row == 9 {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "TermsAndConditionViewController") as! TermsAndConditionViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                    
                }
                    
                else if indexPath.row == self.subMenu.count - 1 {
                    if UserDefaults.standard.value(forKey: "token") != nil {
                        hideSideMenu()
                        self.ApiCallToLogout()
                    }
                    else {
                        hideSideMenu()
                        let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                        let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                        navigationController.pushViewController(viewController, animated: true)
                    }
                }
            }
        }
    }
    
    func tableView(_ tableView: UITableView, viewForFooterInSection section: Int) -> UIView? {
        let dividerView = UIView.init(frame: CGRect.init(x: 0, y: 5, width: tableView.frame.width, height: 1))
        dividerView.backgroundColor = #colorLiteral(red: 0.9215686275, green: 0.9215686275, blue: 0.9215686275, alpha: 1)
        return dividerView
    }
    func tableView(_ tableView: UITableView, heightForFooterInSection section: Int) -> CGFloat {
        if tableView == menuTableView {
            return 1
        } else {
            return 0
        }
    }
}


