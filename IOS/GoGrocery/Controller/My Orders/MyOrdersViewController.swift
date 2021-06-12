import UIKit
import ViewPager_Swift
import SwiftyJSON
class MyOrdersViewController: UIViewController {
    @IBOutlet weak var pagerView: UIView!
     let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var pager:ViewPager?
    let tabs = [
        ViewPagerTab(title: "Present Orders", image: UIImage(named: "")),
        ViewPagerTab(title: "Past Orders", image: UIImage(named: ""))
    ]
    @IBOutlet weak var btncart: UIButton!
    @IBOutlet weak var btnCartCount: UIButton!
       var cartArray = [JSON]()
        var badgeCount = Int()
      var navigationType:String = ""
    
    @IBOutlet weak var navigationView: UIView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        self.navigationView.addShadow1()
        let options = ViewPagerOptions()
        options.tabType = .basic
        options.distribution = .segmented
        options.isTabHighlightAvailable = false
        options.isTabIndicatorAvailable = true
        options.tabViewBackgroundDefaultColor = UIColor.white
        options.tabIndicatorViewBackgroundColor = UIColor.red
        options.tabViewTextDefaultColor = UIColor.black
        pager = ViewPager(viewController: self, containerView: pagerView)
        pager?.setOptions(options: options)
        pager?.setDataSource(dataSource: self)
        pager?.setDelegate(delegate: self)
        pager?.build()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        navigationController?.setNavigationBarHidden(true, animated: true)
       // ApiCallToViewCart()
        //ApiCallToGetCartCount()
    }
    
    @IBAction func cartButtonTapped(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func backButtonTapped(_ sender: Any) {
            if navigationType == "present" {
            dismiss(animated: true, completion: nil)
             // being presented
         }
        else {
              self.navigationController?.popViewController(animated: true)
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
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers,loaderShow: false) { (response: JSON) in
                print(response)
                if response["status"].intValue == 200 {
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    print(self.badgeCount)
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btncart.setImage(UIImage(named: "cart"), for: .normal)
                    //                    self.collectionView.reloadData()
                }
                else {
                    //                    self.cartArra
                    self.btnCartCount.isHidden = true
                    self.btncart.setImage(UIImage(named: "cart"), for: .normal)
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
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "view-cart/", vc: self, header: headers,loaderShow: false) { (response: JSON) in
                print(response)
                if response["status"].intValue == 200 {
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btncart.setImage(UIImage(named: "cart"), for: .normal)
                }
                else {
                    self.btnCartCount.isHidden = true
                    self.btncart.setImage(UIImage(named: "cart"), for: .normal)
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
            getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: "cart-count/", vc: self, header: headers,loaderShow: false) { (response: JSON) in
                 print(response)
                if response["cart_count"].intValue > 0 {
                    self.ApiCallToViewCart()
                }
                else {
                    self.btnCartCount.isHidden = true
                    self.btncart.setImage(UIImage(named: "cart"), for: .normal)
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
                    self.btncart.setImage(UIImage(named: "cart"), for: .normal)
                }
                
            }
        }
    }
    
}

extension MyOrdersViewController: ViewPagerDataSource {
    func numberOfPages() -> Int {
        return 2
    }
    func viewControllerAtPosition(position:Int) -> UIViewController {
        if position == 0 {
            let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "PresentOrdersViewController") as! PresentOrdersViewController
            
            return vc
        } else {
            let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "PastOrdersViewController") as! PastOrdersViewController
            
            return vc
        }
        
    }
    
    func tabsForPages() -> [ViewPagerTab] {
        return tabs
    }
    
    func startViewPagerAtIndex() -> Int {
        return 0
    }
}

extension MyOrdersViewController: ViewPagerDelegate {
    
    func willMoveToControllerAtIndex(index:Int) {
        print("Moving to page \(index)")
    }
    
    func didMoveToControllerAtIndex(index: Int) {
        print("Moved to page \(index)")
    }
}
