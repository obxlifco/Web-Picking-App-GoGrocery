
import UIKit
import SwiftyJSON
import FirebaseAnalytics
class ProductListingViewController: UIViewController ,SelectFilterDelegate, UIScrollViewDelegate {
    @IBOutlet weak var btnFilter: UIButton!
    @IBOutlet weak var btnSort: UIButton!
    @IBOutlet weak var filterView: UIView!
    @IBOutlet weak var collectionView: UICollectionView!
    @IBOutlet weak var lblTitle: UILabel!
    @IBOutlet weak var btnCart: UIButton!
    @IBOutlet weak var btnCartCount: UIButton!
    @IBOutlet weak var navigationView: UIView!
    var screenSize: CGRect!
    var screenWidth: CGFloat!
    var screenHeight: CGFloat!
    var filterText = String()
    var titleString = String()
    var productTitle = String()
    var slugInListing = String()
    var type = String()
    var mustNotArray = [[String:Any]]()
    var sortArray = [[String:Any]]()
    var mustArray = [[String:Any]]()
    var filterArray = [[String:Any]]()
    private let spacing:CGFloat = 1
    var bArray = [Int]()
    var cArray = [Int]()
    var productArray = [JSON]()
    var count = Int()
    var cartDatafromDb = [AddcCart]()
    var productId = Int()
    var quantity = Int()
    var from = Int()
    var to = Int()
    var isNewDataLoading =  Bool()
    var brandBool = Bool()
    var brandIDD = [Int]()
    var cartArray = [JSON]()
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var sideMenuBool = Bool()
    var badgeCount = Int()
    var sortSelect = Bool()
    var filterBool = Bool()
    var isFirstTime:Bool = true
    var isSortBool:Bool = true
    var firstElastic = Bool()
    var jsonFromSearch = [String:Any]()
    var isFirstTimefromSearch = Bool()
    var productIdArray = [Int]()
    var isFilterFromSearchElasticInListing = Bool()
    var requiredJson: [String: Any] = [:]
    var isBrandSelect = Bool()
    var mustArrayFromSearch = [[String:Any]]()
    var filterArrayFromSearch = [[String:Any]]()
    @IBOutlet weak var noProductView: UIView!
    var searchSortBool:Bool = false
    var scrollbaleBool = false
    var searchFromFilterFirstTimeCheck:Bool = false
    var isFilterFromSearchElasticInListingCopy:Bool = false
    var slugDictInListing :[String:Any] = [:]
    var navigationType:String = ""
    var yearCheck = String()
    @IBOutlet weak var noProductViewHeight: NSLayoutConstraint!
    @IBOutlet weak var imgSad: UIImageView!
    @IBOutlet weak var lblNoProduct: UILabel!
    
    
    //    MARK:- View Life Cycle
    override func viewDidLoad() {
        super.viewDidLoad()
        
      //  ApiCallToGetproductListing()
        self.filterView.addShadow1()
        btnCartCount.layer.cornerRadius = btnCartCount.frame.height/2
        filterText = "desc"
        count = 0
        let layout = UICollectionViewFlowLayout()
        layout.sectionInset = UIEdgeInsets(top: spacing, left: spacing, bottom: spacing, right: spacing)
        layout.minimumLineSpacing = spacing
        layout.minimumInteritemSpacing = spacing
        self.collectionView?.collectionViewLayout = layout
        btnSort.layer.cornerRadius = 5
        btnFilter.layer.cornerRadius = 5
        self.lblTitle.text = productTitle
        from = 0
        to = 18
        filterText = "desc"
        self.productArray.removeAll()
        ApiCallToGetproductListing()
        self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
        ViewProductInListing()
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
       // self.collectionView.reloadData()
        self.ApiCallToViewCart()
        noProductView.isHidden = true
        //self.ApiCallToGetCartCount()
        //self.collectionView.reloadData()
        self.navigationController?.isNavigationBarHidden = true
        self.navigationView.addShadow1()
        self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
    }
    
    func ViewProductInListing() {
        Analytics.logEvent("View Product", parameters: [:])
    }
    
    @IBAction func btnBackAction(_ sender: Any) {
        print(isBeingPresented)
        print(isMovingToParent)
        if navigationType == "present" {
            dismiss(animated: true, completion: nil)
            // being presented
        }
        else {
            self.navigationController?.popViewController(animated: true)
        }
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
    
    @objc func filterTapped() {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    
    //    MARK:- Button Action
    @IBAction func btnSortAction(_ sender: Any) {
        setUpSortXibFunc()
    }
    
    @IBAction func btnFilterAction(_ sender: Any) {
        if isFirstTimefromSearch == true {
            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "FilterViewController") as! FilterViewController
            vc.slugInListingInFilter = slugInListing
            vc.typeInFilter = type
            vc.productIdArrayFromSearch = productIdArray
            vc.isFilterFromSearch = false
            vc.delegate = self
            vc.isFilterFromSearch = true
            self.navigationController?.pushViewController(vc, animated: true)
        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "FilterViewController") as! FilterViewController
            vc.slugInListingInFilter = slugInListing
            vc.typeInFilter = type
            vc.productIdArrayFromSearch = productIdArray
            vc.isFilterFromSearch = false
            vc.delegate = self
            vc.isBrandSelectInFilter = isBrandSelect
            self.navigationController?.pushViewController(vc, animated: true)
        }
    }
    
    func filterSelect(catArr: [Int], isCategoryBool: Bool, isBrandSelect: Bool, brandArr: [Int], isFilterFromSearchElastic: Bool) {
        if isFilterFromSearchElastic == true {
            self.isFilterFromSearchElasticInListingCopy = isFilterFromSearchElastic
            isFilterFromSearchElasticInListing = isFilterFromSearchElastic
            self.mustArray.removeAll()
            isFirstTime = false
            let isDeletedDict = ["match" :["isdeleted" : "n"]]
            let isBlockedDict = ["match" :["isblocked" : "n"]]
            let isVisibleDict = ["match" :["visibility_id":["query": "Catalog Search", "operator": "and"]]]
            //            self.mustArray.append
            self.mustArray.append(isDeletedDict)
            self.mustArray.append(isBlockedDict)
            self.mustArray.append(isVisibleDict)
            if brandArr.count != 0 {
                let brandDict = ["terms" : ["brand_id" : brandArr]]
                self.mustArray.append(brandDict)
            }
            if catArr.count != 0 {
                let categoryIdDict = ["terms" : ["category_id" : catArr]]
                self.mustArray.append(categoryIdDict)
            }
            self.filterArray.removeAll()
            let filterFirst = ["nested": ["path": "inventory" , "score_mode": "avg", "query": ["bool" :["must": [["term" :["inventory.id" : wareHouseId] ],["range" : ["inventory.stock" : ["gt" : 0]]]]]]] ]
            let filterSecond = ["nested" : ["path": "channel_currency_product_price" , "query": [["bool":["must": [["range": ["channel_currency_product_price.new_default_price" : ["gt":0]]],["term":["channel_currency_product_price.warehouse_id" : wareHouseId]]]]]]]]
            let filterThird  = ["nested": ["path": "product_images","query":["bool":["must":[["term" : ["product_images.is_cover":1]]]]]]]
            let filterFourth = ["terms":["id":self.productIdArray]]
            self.filterArray.append(filterFirst)
            self.filterArray.append(filterSecond)
            self.filterArray.append(filterThird)
            self.filterArray.append(filterFourth)
            self.sortArray.removeAll()
            self.filterText = "desc"
            let sortDict = ["category": ["order":filterText]]
            self.sortArray.append(sortDict)
            self.mustNotArray.removeAll()
            let mustNotDict = ["term":["product_images.img" : " "]]
            mustNotArray.append(mustNotDict)
            self.from = 0
            self.to = 18
            self.productArray.removeAll()
            collectionView.reloadData()
            ApiCallToGetproductListing()
        }
        else {
            self.bArray.removeAll()
            self.cArray.removeAll()
            self.mustArray.removeAll()
            self.mustNotArray.removeAll()
            self.filterArray.removeAll()
            self.bArray = brandArr
            self.cArray = catArr
            isFirstTime = true
            self.productArray.removeAll()
            collectionView.reloadData()
            self.from = 0
            self.to = 18
            ApiCallToGetproductListing()
            isFirstTime = false
            //             isFirstTime = false
        }
        
    }
    
    
    //    MARK:- Sorting Xib
    func setUpSortXibFunc () {
        requestsortView(vc: self)
        
        sortXib.btnNewArrival.addTarget(self, action: #selector(btnPopularityAction), for: .touchUpInside)
        sortXib.btnPriceHighToLowFull.addTarget(self, action: #selector(btnPriceHighToLowAction), for: .touchUpInside)
        sortXib.priceLowToHighFull.addTarget(self, action: #selector(btnPriceLowToHighAction), for: .touchUpInside)
        sortXib.btnCancel.addTarget(self, action: #selector(btnCancelAction), for: .touchUpInside)
        sortXib.btnApply.addTarget(self, action: #selector(btnApplyAction), for: .touchUpInside)
        
        sortXib.sortView.layer.shadowColor = UIColor.lightGray.cgColor
        sortXib.sortView.layer.shadowOpacity = 0.5
        sortXib.sortView.layer.shadowOffset = .zero
        sortXib.sortView.layer.cornerRadius = 5
        sortXib.sortView.layer.shadowRadius = 0.5
        sortXib.sortView.layer.shadowPath = UIBezierPath(rect: sortXib.sortView.bounds).cgPath
        sortXib.sortView.layer.shouldRasterize = true
        sortXib.sortView.layer.rasterizationScale = UIScreen.main.scale
    }
    //    MARK:- Button Related Functions
    
    @objc func btnPopularityAction() {
        btnPopularitySelect()
    }
    @objc func btnPriceHighToLowAction() {
        btnPriceHighToLowSelect()
    }
    @objc func btnPriceLowToHighAction() {
        btnPriceLowToHighSelect()
    }
    @objc func btnCancelAction() {
        sortXib.removeFromSuperview()
        sortSelect =  false
    }
    @objc func btnApplyAction() {
        sortXib.removeFromSuperview()
        self.sortArray.removeAll()
        let sortDict = ["channel_currency_product_price.new_default_price": ["order":filterText, "mode": "avg", "nested_path" : "channel_currency_product_price","nested_filter":["term":["channel_currency_product_price.warehouse_id":wareHouseId]]]]
        self.sortArray.append(sortDict)
        print(sortDict)
        isFirstTime = false
        self.productArray.removeAll()
        collectionView.reloadData()
        if isFirstTimefromSearch == true {
            self.searchSortBool = true
            self.from = 0
            ApiCallToGetproductListing()
        }
        else if self.isFilterFromSearchElasticInListingCopy == true {
            isFilterFromSearchElasticInListing = true
            isFirstTimefromSearch = true
            self.from = 0
            ApiCallToGetproductListing()
        }
        else if isFilterFromSearchElasticInListing == false {
            isFirstTimefromSearch = false
            isFilterFromSearchElasticInListing  = true
            self.from = 0
            ApiCallToGetproductListing()
            //              self.searchSortBool = true
        }
        else {
            self.searchSortBool = false
            self.from = 0
            ApiCallToGetproductListing()
        }
    }
    
    //    MARK:- Filter Select Functions
    func btnPopularitySelect() {
        AllUnselect()
        sortXib.btnPopularity.setImage(UIImage(named: "radio_select"), for: .normal)
        filterText = "desc"
        sortSelect = true
        
    }
    func btnPriceHighToLowSelect() {
        AllUnselect()
        sortXib.btnPriceHighToLow.setImage(UIImage(named: "radio_select"), for: .normal)
        filterText = "desc"
        sortSelect = true
    }
    func btnPriceLowToHighSelect() {
        AllUnselect()
        sortXib.btnPriceLowToHigh.setImage(UIImage(named: "radio_select"), for: .normal)
        filterText = "asc"
        sortSelect = true
    }
    func AllUnselect() {
        sortXib.btnPopularity.setImage(UIImage(named: "radio_unselect"), for: .normal)
        sortXib.btnPriceHighToLow.setImage(UIImage(named: "radio_unselect"), for: .normal)
        sortXib.btnPriceLowToHigh.setImage(UIImage(named: "radio_unselect"), for: .normal)
        filterText = " "
    }
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
        guard  scrollbaleBool == true else  {
            scrollbaleBool = true
            return
        }
        let offset = scrollView.contentOffset
        let bounds = scrollView.bounds
        let size = scrollView.contentSize
        let inset = scrollView.contentInset
        let y = offset.y + bounds.size.height - inset.bottom
        let h = size.height
        let reload_distance:CGFloat = 10.0
        if y > (h + reload_distance) {
            print("load more rows")
            if !isNewDataLoading {
                isNewDataLoading = true
                self.from = from + 18
                self.to = 18
                //if isSort
                isFirstTime = false
                ApiCallToGetproductListing()
            }
        }
    }
    
    //    MARK:- View Cart
    func ApiCallToGetproductListing() {
        
        if isFirstTime
        {
            
            let isDeletedDict = ["match" :["isdeleted" : "n"]]
            let isBlockedDict = ["match" :["isblocked" : "n"]]
            let isVisibleDict = ["match" :["visibility_id":["query": "Catalog Search", "operator": "and"]]]
            let categoryDict =  ["terms" : ["category_slug.keyword" : [slugInListing]]]
            let categoryDict1 =  ["terms" : ["brand_slug.keyword" : [slugInListing]]]
            
            let categoryIdDict = ["terms" : ["category_id" : self.cArray]]
            let brandDict = ["terms" : ["brand_id" : self.bArray]]
            let filterFirst = ["nested": ["path": "inventory" , "score_mode": "avg", "query": ["bool" :["must": [["term" :["inventory.id" : wareHouseId] ],["range" : ["inventory.stock" : ["gt" : 0]]]]]]] ]
            
            let filterSecond = ["nested" : ["path": "channel_currency_product_price" , "query": [["bool":["must": [["range": ["channel_currency_product_price.new_default_price" : ["gt":0]]],["term":["channel_currency_product_price.warehouse_id" : wareHouseId]]]]]]]]
            let mustNotDict = ["term":["product_images.img" : " "]]
            mustNotArray.append(mustNotDict)
            self.sortArray.removeAll()
            let sortDict = ["category": ["order":filterText]]
            self.sortArray.append(sortDict)
            print(sortDict)
            let filterThird  = ["nested": ["path": "product_images","query":["bool":["must":[["term" : ["product_images.is_cover":1]]]]]]]
            
            if bArray.count != 0 {
                mustArray.append(brandDict)
            }
            if cArray.count != 0 {
                mustArray.append(categoryIdDict)
            }
            mustArray.append(isDeletedDict)
            mustArray.append(isBlockedDict)
            mustArray.append(isVisibleDict)
            if brandBool == true {
                mustArray.append(categoryDict1)
            }
            else {
                mustArray.append(categoryDict)
            }
            filterArray.append(filterFirst)
            filterArray.append(filterSecond)
            filterArray.append(filterThird)
            //   let requiredJson: [String: Any]  = ["query": ["bool" :["must" : mustArray, "filter" : filterArray, "must_not": mustNotArray]], "from": from ,"size": "18" , "sort" : sortArray ] // Live
            
            let requiredJson: [String: Any]  = ["table_name":"EngageboostProducts" , "website_id" : "1", "data" : ["query": ["bool" :["must" : mustArray, "filter" : filterArray, "must_not": mustNotArray]], "from": from ,"size": "18" , "sort" : sortArray ] ]// Demo
            
            print(requiredJson)
            let jsonData = try! JSONSerialization.data(withJSONObject: requiredJson)
            let jsonString = String(data: jsonData, encoding: .utf8)
            print(jsonString ?? "Wrong data")
            postMethodQuery1(apiName: searchElasticApi, params: requiredJson, vc: self) { (response : JSON) in
                print(response)
                let testProductArray = response["hits"]["hits"].arrayValue
                if testProductArray.count != 0 {
                    self.productArray.append(contentsOf: testProductArray)
                    self.isNewDataLoading = false
                    self.noProductView.isHidden = true
                    self.filterView.isHidden = false
                    self.collectionView.dataSource = self
                    self.collectionView.delegate = self
                    self.collectionView.reloadData()
                }
                else {
                    self.noProductView.isHidden = false
                    self.noProductViewHeight.constant = 150
                    self.lblNoProduct.text = "No Product Found!"
                    self.imgSad.image = UIImage(named: "sad")
                    self.lblNoProduct.isHidden = false
                    self.imgSad.isHidden = false
                    self.filterView.isHidden = true
                }
            }
        }
          
        else if isFirstTimefromSearch {
            if isFilterFromSearchElasticInListing == true {
                //   requiredJson  = ["query": ["bool" :["must" : mustArray, "filter" : filterArray, "must_not": mustNotArray]], "from": from ,"size": "18" , "sort" : sortArray ] //Live
                let requiredJson: [String: Any]  = ["table_name":"EngageboostProducts" , "website_id" : "1", "data" : ["query": ["bool" :["must" : mustArray, "filter" : filterArray, "must_not": mustNotArray]], "from": from ,"size": "18" , "sort" : sortArray ] ]// Demo
                print(requiredJson)
                let jsonData = try! JSONSerialization.data(withJSONObject: requiredJson)
                let jsonString = String(data: jsonData, encoding: .utf8)
                print(jsonString ?? "Wrong data")
                postMethodQuery1(apiName: searchElasticApi, params: requiredJson, vc: self) { (response : JSON) in
                    print(response)
                    let testProductArray = response["hits"]["hits"].arrayValue
                    if testProductArray.count != 0 {
                        self.productArray.append(contentsOf: testProductArray)
                        self.isNewDataLoading = false
                        self.searchFromFilterFirstTimeCheck = true
                        self.collectionView.dataSource = self
                        self.collectionView.delegate = self
                        self.noProductView.isHidden = true
                        self.filterView.isHidden = false
                        self.collectionView.reloadData()
                        
                    }
                    else {
                        if self.searchFromFilterFirstTimeCheck == false {
                            self.noProductView.isHidden = false
                            self.filterView.isHidden = true
                            self.noProductViewHeight.constant = 150
                            self.lblNoProduct.text = "No Product Found!"
                            self.imgSad.image = UIImage(named: "sad")
                            self.lblNoProduct.isHidden = false
                            self.imgSad.isHidden = false
                            self.searchFromFilterFirstTimeCheck = true
                        }
                        
                    }
                }
            }
            else {
                var requiredJsonTemp: [String: Any] = [:]
                if  self.searchSortBool == true {
                    
                    requiredJson = ["table_name":"EngageboostProducts" , "website_id" : "1", "data" : ["query": ["bool" :["must" : mustArrayFromSearch, "filter" : filterArrayFromSearch]], "from": from ,"size": "18" , "sort" : sortArray ] ]// Demo
                    //  requiredJsonTemp = ["query": ["bool" :["must" : mustArrayFromSearch, "filter" : filterArrayFromSearch]], "from": from ,"size": "18" ,"sort" : sortArray] // Live
                   // requiredJson  = requiredJsonTemp
                    print(requiredJson)
                    let jsonData = try! JSONSerialization.data(withJSONObject: requiredJson)
                    let jsonString = String(data: jsonData, encoding: .utf8)
                    print(jsonString ?? "Wrong data")
                    //                   // let api = "http://15.185.126.44:8062/api/search_elastic/" //demo
                    //                    let api = "https://www.gogrocery.ae/elastic/lifco1_product_1/data/_search" //live
                    postMethodQuery1(apiName: searchElasticApi, params: requiredJson, vc: self) { (response : JSON) in
                        print(response)
                        let testProductArray = response["hits"]["hits"].arrayValue
                        if testProductArray.count != 0 {
                            for index in testProductArray {
                                let productId = index["_id"].intValue
                                self.productIdArray.append(productId)
                            }
                            self.productArray.append(contentsOf: testProductArray)
                            self.isNewDataLoading = false
                            self.collectionView.dataSource = self
                            self.collectionView.delegate = self
                            self.collectionView.reloadData()
                        }
                        else {
                        }
                    }
                }
                else {
                    requiredJson = ["table_name":"EngageboostProducts" , "website_id" : "1", "data" : ["query": ["bool" :["must" : mustArrayFromSearch, "filter" : filterArrayFromSearch]], "from": from ,"size": "18" ] ]// Demo
                    
                    //     requiredJsonTemp = ["query": ["bool" :["must" : mustArrayFromSearch, "filter" : filterArrayFromSearch]], "from": from ,"size": "18"] // Live
                   // requiredJson  = requiredJsonTemp
                    print(requiredJson)
                    let jsonData = try! JSONSerialization.data(withJSONObject: requiredJson)
                    let jsonString = String(data: jsonData, encoding: .utf8)
                    print(jsonString ?? "Wrong data")
                    //                   // let api = "http://15.185.126.44:8062/api/search_elastic/" //demo
                    //                    let api = "https://www.gogrocery.ae/elastic/lifco1_product_1/data/_search" //live
                    postMethodQuery1(apiName: searchElasticApi, params: requiredJson, vc: self) { (response : JSON) in
                        print(response)
                        let testProductArray = response["hits"]["hits"].arrayValue
                        if testProductArray.count != 0 {
                            for index in testProductArray {
                                let productId = index["_id"].intValue
                                self.productIdArray.append(productId)
                            }
                            self.productArray.append(contentsOf: testProductArray)
                            self.isNewDataLoading = false
                            self.collectionView.dataSource = self
                            self.collectionView.delegate = self
                            self.noProductView.isHidden = true
                            self.filterView.isHidden = false
                            self.collectionView.reloadData()
                        }
                        else {
                            if self.productArray.count == 0 {
                                self.noProductView.isHidden = false
                                self.noProductViewHeight.constant = 150
                                self.lblNoProduct.text = "No Product Found!"
                                self.lblNoProduct.isHidden = false
                                self.imgSad.isHidden = false
                                self.imgSad.image = UIImage(named: "sad")
                                self.filterView.isHidden = true
                            }
                            else {
                                
                            }
                            
                        }
                    }
                }
            }
        }
        else {
            
            // let requiredJson: [String: Any]  = ["query": ["bool" :["must" : mustArray, "filter" : filterArray, "must_not": mustNotArray]], "from": from ,"size": "18" , "sort" : sortArray] // Live
            
            //  let requiredJson: [String: Any]  = ["table_name": "EngageboostProducts", "website_id": 1,"query": ["bool" :["must" : mustArray, "filter" : filterArray, "must_not": mustNotArray]], "from": from ,"size": "18" , "sort" : sortArray ]
            
            let requiredJson: [String: Any]  = ["table_name":"EngageboostProducts" , "website_id" : "1", "data" : ["query": ["bool" :["must" : mustArray, "filter" : filterArray, "must_not": mustNotArray]], "from": from ,"size": "18" , "sort" : sortArray ] ]// Demo
            
            print(requiredJson)
            let jsonData = try! JSONSerialization.data(withJSONObject: requiredJson)
            let jsonString = String(data: jsonData, encoding: .utf8)
            print(jsonString ?? "Wrong data")
            //            let api = "http://15.185.126.44:8062/api/search_elastic/" //demo
            //           //   let api = "https://www.gogrocery.ae/elastic/lifco1_product_1/data/_search" //live
            postMethodQuery1(apiName: searchElasticApi, params: requiredJson, vc: self) { (response : JSON) in
                print(response)
                let testProductArray = response["hits"]["hits"].arrayValue
                if testProductArray.count != 0 {
                    for index in testProductArray {
                        let productId = index["_id"].intValue
                        self.productIdArray.append(productId)
                    }
                    
                    self.productArray.append(contentsOf: testProductArray)
                    self.isNewDataLoading = false
                    self.collectionView.dataSource = self
                    self.collectionView.delegate = self
                    self.collectionView.reloadData()
                }
                else {
                    print("No Products to display")
                }
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
//                    self.collectionView.dataSource = self
//                    self.collectionView.delegate = self
                   //  self.collectionView.reloadData()
                }
                else {
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    self.collectionView.dataSource = self
                    self.collectionView.delegate = self
                    //self.collectionView.reloadData()
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
                     //self.collectionView.reloadData()
                }
                else {
                    self.btnCartCount.isHidden = true
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                     //self.collectionView.reloadData()
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
        
//        if ageString == "N" {
//             yearCheck = "N"
//        }
       // else {
            yearCheck = ageString
            self.count = count + 1
            var superview = sender.superview
            while let view = superview, !(view is UICollectionViewCell) {
                superview = view.superview
            }
            guard let cell = superview as? UICollectionViewCell else {
                return
            }
            guard let indexPath = collectionView.indexPath(for: cell) else {
                return
            }
            guard let cell1 = superview as? ProductListingCollectionViewCell else {
                return
            }
            let productDict = productArray[indexPath.row].dictionaryValue
            print(productDict)
            productId = productDict["_id"]!.intValue
            quantity = count
            
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var auth = String()
            if (UserDefaults.standard.value(forKey: "is-login") != nil){
                auth = (UserDefaults.standard.value(forKey: "token") as! String)
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
                        self.ApiCallToViewCart()
                        let sourceDict = productDict["_source"]?.dictionaryValue
                        let contentName  = sourceDict!["name"]?.stringValue
                        let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName!]
                        AddCart(dictParam: dictParam)
                        logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName!, currency: "AED", valueToSum: cost)
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
                params["product_id"] = productId
                params["quantity"] = quantity
                params["year_check"] = yearCheck
                postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
                    if response["status"].intValue == 1 {
                        let cartDict = response["cart_data"].dictionaryValue
                        let count1 = cartDict["cartdetails"]![0]["qty"].intValue
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
                           self.ApiCallToViewCart()
                        let sourceDict = productDict["_source"]?.dictionaryValue
                        let contentName  = sourceDict!["name"]?.stringValue
                        let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName!]
                        print(dictParam)
                        AddCart(dictParam: dictParam)
                        logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName!, currency: "AED", valueToSum: cost)
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
       
        
//        if UserDefaults.standard.value(forKey: "") == nil ||  UserDefaults.standard.value(forKey: "") as?  == "Y" {
//            if UserDefaults.standard.value(forKey: "Age_Check") as! String == "Y" {
//
//            }
//            else {
//
//            }
//        }
        

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
        var superview = sender.superview
        while let view = superview, !(view is UICollectionViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UICollectionViewCell else {
            return
        }
        guard let indexPath = collectionView.indexPath(for: cell) else {
            return
        }
        guard let cell1 = superview as? ProductListingCollectionViewCell else {
            return
        }
        let productDict = productArray[indexPath.row].dictionaryValue
        let productId = "\(productDict["_id"]!.intValue)"
        
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
                    self.ApiCallToViewCart()
                    let sourceDict = productDict["_source"]?.dictionaryValue
                    let contentName  = sourceDict!["name"]?.stringValue
                   let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName!]
                    print(dictParam)
                    AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName!, currency: "AED", valueToSum: cost)
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
                    let msg = response["msg"].stringValue
                    createalert(title: "Alert", message: msg, vc: self)
                }
            }
        }
        else {
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = newProductId
            params["quantity"] = newQuantity
            params["year_check"] = yearCheck
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
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
                    self.ApiCallToViewCart()
                    let sourceDict = productDict["_source"]?.dictionaryValue
                    let contentName  = sourceDict!["name"]?.stringValue
                   let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":"product","Currency":"AED","ValueToSum":"\(cost)","content_name":contentName!]
                    print(dictParam)
                    AddCart(dictParam: dictParam)
                    logAddToCartEvent(content_ID: "\(self.productId)", content_Type: contentName!, currency: "AED", valueToSum: cost)
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
        var superview = sender.superview
        while let view = superview, !(view is UICollectionViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UICollectionViewCell else {
            //    print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = collectionView.indexPath(for: cell) else {
            //    print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? ProductListingCollectionViewCell else {
            //    print("rferffddvd")
            return
        }
        // We've got the index path for the cell that contains the button, now do something with it.
        let productDict = productArray[indexPath.row].dictionaryValue
        let productId = "\(productDict["_id"]!.intValue)"
        for (index, element) in cartDatafromDb.enumerated() {
            // print("Item \(index): \(element)")
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                var inttype: Int = Int(quantt)!
                inttype = inttype - 1
                newQuantity = inttype
                cell1.btnMinus.isHidden = false
                cell1.btnPlus.isHidden = false
                tempCost = element.cost
            }
            else {
                cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                cell1.btnMinus.isHidden = true
                cell1.btnPlus.isHidden = true
            }
        }
        var auth = String()
        if (UserDefaults.standard.value(forKey: "is-login") != nil){
            auth = (UserDefaults.standard.value(forKey: "token") as! String)
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
                    self.ApiCallToViewCart()
                    let sourceDict = productDict["_source"]?.dictionaryValue
                    let contentName  = sourceDict!["name"]?.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName!,"Currency":"AED","ValueToSum":cost]
                    print(dictParam)
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

//                    let msg = response["msg"].stringValue
//                    createalert(title: "Alert", message: msg, vc: self)
                }
            }
        }
        else {
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            var params = [String:Any]()
            params["device_id"] = deviceID
            params["product_id"] = newProductId
            params["quantity"] = newQuantity
            params["year_check"] = yearCheck
            postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
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
                    self.ApiCallToViewCart()
                    let sourceDict = productDict["_source"]?.dictionaryValue
                    let contentName  = sourceDict!["name"]?.stringValue
                    let dictParam :[String:Any] = ["Content_ID":"\(self.productId)","Content_Type":contentName!,"Currency":"AED","ValueToSum":cost]
                    print(dictParam)
                    //  self.ReduceCart(product_id: newProductId)
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
    
    @objc func addToSaveListAction(sender: UIButton) {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let tag = sender.tag
            let productDict = productArray[tag].dictionaryValue
            let productId = productDict["_id"]!.intValue
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
}
extension UIImage {
    func imageWithInsets(insets: UIEdgeInsets) -> UIImage? {
        UIGraphicsBeginImageContextWithOptions(
            CGSize(width: self.size.width + insets.left + insets.right,
                   height: self.size.height + insets.top + insets.bottom), false, self.scale)
        let _ = UIGraphicsGetCurrentContext()
        let origin = CGPoint(x: insets.left, y: insets.top)
        self.draw(at: origin)
        let imageWithInsets = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        return imageWithInsets
    }
}

//MARK:- CollectionView Delegate
extension ProductListingViewController : UICollectionViewDelegate, UICollectionViewDataSource  {
    
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return productArray.count
    }
    
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "ProductListingCollectionViewCell", for: indexPath) as! ProductListingCollectionViewCell
        
        if isFirstTimefromSearch {
            let productDict = productArray[indexPath.row].dictionaryValue
            let productId = productDict["_id"]!.intValue
            self.productIdArray.append(productId)
            
        }
        cell.btnSave.tag = indexPath.row
        cell.btnSave.addTarget(self, action: #selector(addToSaveListAction), for: .touchUpInside)
        let productDict = productArray[indexPath.row].dictionaryValue
        let sourceDict = productDict["_source"]?.dictionaryValue
        if let brandName = sourceDict!["brand"]?.string {
            cell.lblBrand.text = brandName
        }
        else {
            cell.lblBrand.isHidden = true
        }
        let weight = sourceDict!["weight"]!.intValue
        let unit = sourceDict!["unit"]!.stringValue
        cell.lblProductWeight.text = "\(weight)\(unit)"
        let productImagesArray = sourceDict!["product_images"]?.arrayValue
        if productImagesArray?.count != 0 {
            let imageDict = productImagesArray![0].dictionaryValue
            let url = imageDict["link"]?.stringValue
            if let brandurl = imageDict["img"]?.stringValue{
                let fullUrl = url! + brandurl
                let url = URL(string: fullUrl)
                cell.imgImage.sd_setImage(with: url!)
                cell.imgImage.image?.withAlignmentRectInsets(UIEdgeInsets(top: -25, left: -25, bottom: -25, right: -25))
                
                // resizeImage
            }
        }
        else {
            cell.imgImage.image? = UIImage(named:"no_image")!
            // cell.imgImage.image?.withAlignmentRectInsets(UIEdgeInsets(top: -25, left: -25, bottom: -25, right: -25))
        }
        
        DispatchQueue.main.async {
            
            let priceArr = sourceDict!["channel_currency_product_price"]!.arrayValue
            for index in priceArr {
                if index["warehouse_id"].intValue == self.wareHouseId && index["price_type"].intValue == 1 {
                    let price = index["new_default_price_unit"].doubleValue
                    let doubleStr = String(format: "%.2f", price) // "3.14"
                    print(doubleStr)
                    cell.lblOrignalPrice.text = "AED \(doubleStr)"
                    if index["discount_amount"].intValue > 0 {
                        cell.lblDiscount.text = "\(index["discount_amount"].intValue)% OFF"
                        cell.lblDiscount.isHidden = false
                        let sp = index["mrp"].doubleValue
                        let doubleStr1 = String(format: "%.2f", sp)
                        let doubleStr2 = "AED \(doubleStr1)"
                        
                        let attributeString: NSMutableAttributedString =  NSMutableAttributedString(string: doubleStr2)
                        attributeString.addAttribute(NSAttributedString.Key.strikethroughStyle, value: 2, range: NSMakeRange(0, attributeString.length))
                        cell.lblStrikedPrice.attributedText = attributeString
                        cell.lblStrikedPrice.isHidden = false
                    }
                    else {
                        cell.lblDiscount.isHidden = true
                        cell.lblStrikedPrice.isHidden = true
                    }
                }
            }
            cell.lblTitle.text = sourceDict!["name"]?.stringValue
        }
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
        let productDict1 = productArray[indexPath.row].dictionaryValue
        let productId = "\(productDict1["_id"]!.intValue)"
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
 
    /*    if self.cartArray.count != 0 {
            for index in self.cartArray {
                let cartProductIdDict = index["product_id"].dictionaryValue
                let cartProductId = cartProductIdDict["id"]?.int ?? 0
                if productId == cartProductId {
                     let quant = index["quantity"].int ?? 0
                      //  let inttype: Int = Int(quant) ?? 0
                        DispatchQueue.main.async {
                            cell.btnAddtoCart.setTitle("\(quant)", for: .normal)
                            cell.btnAddtoCart.backgroundColor = .white
                            cell.btnAddtoCart.setTitleColor(.black, for: .normal)
                            cell.btnMinus.isHidden = false
                            cell.btnPlus.isHidden = false
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
        else {
            cell.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
            cell.btnAddtoCart.backgroundColor = .clear
            cell.btnAddtoCart.setTitleColor(.white, for: .normal)
            cell.btnMinus.isHidden = true
            cell.btnPlus.isHidden = true
        }
 */

        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        let productDict = productArray[indexPath.row].dictionaryValue
        let sourceDict = productDict["_source"]!.dictionaryValue
        print("tapped")
        print(sourceDict)
        let slug = sourceDict["slug"]!.stringValue
        let productId = productDict["_id"]!.intValue
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
        vc.slugInDetail = slug
        vc.prId = productId
        
        if navigationType == "present" {
            let backButton = UIBarButtonItem()
            backButton.title = ""
            navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
            UINavigationBar.appearance().tintColor = UIColor.black
            navigationController?.pushViewController(vc, animated: true)
        }
        else {
            let backButton = UIBarButtonItem()
            backButton.title = ""
            navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
            UINavigationBar.appearance().tintColor = UIColor.black
            navigationController?.pushViewController(vc, animated: true)
        }
    }
    //    MARK:- Alert
    func showAlert32(message: String)
    {
        let alert = UIAlertController(title: "Alert", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
        }))
        self.present(alert, animated: true, completion: nil)
    }
}
extension ProductListingViewController: UICollectionViewDelegateFlowLayout{
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 1
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let numberOfItemsPerRow:CGFloat = 2
        let spacingBetweenCells:CGFloat = 1
        
        let totalSpacing = (2 * self.spacing) + ((numberOfItemsPerRow - 1) * spacingBetweenCells) //Amount of total spacing in a row
        
        if let collection = self.collectionView{
            let width = (collection.bounds.width - totalSpacing)/numberOfItemsPerRow
            return CGSize(width: width, height: 320)
        }
        else{
            return CGSize(width: 0, height: 0)
        }
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 1
    }
    //    collectionViewprefe
    
}
extension UIImage {
    func imageWithInsets(insetDimen: CGFloat) -> UIImage {
        return imageWithInset(insets: UIEdgeInsets(top: insetDimen, left: insetDimen, bottom: insetDimen, right: insetDimen))
    }
    
    func imageWithInset(insets: UIEdgeInsets) -> UIImage {
        UIGraphicsBeginImageContextWithOptions(
            CGSize(width: self.size.width + insets.left + insets.right,
                   height: self.size.height + insets.top + insets.bottom), false, self.scale)
        let origin = CGPoint(x: insets.left, y: insets.top)
        self.draw(at: origin)
        let imageWithInsets = UIGraphicsGetImageFromCurrentImageContext()?.withRenderingMode(self.renderingMode)
        UIGraphicsEndImageContext()
        return imageWithInsets!
    }
    
}

