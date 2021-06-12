//
//  SidemenuController.swift
//  AKDrawer
//
//  Created by macmini3 on 07/08/19.
//  Copyright © 2019 Gatisofttech. All rights reserved.
//

import UIKit
import SwiftyJSON
class SidemenuController: UIViewController {
    //MARK:- IBOUTLETS
    
    @IBOutlet weak var imgUser: UIImageView!
    @IBOutlet weak var lblUsername: UILabel!
    @IBOutlet weak var colSidemenu: UICollectionView!
    @IBOutlet weak var lblMobile: UILabel!
    
    //MARK:- DECLARATIONS
    
    var SideMenuHeaderArr = [JSON]()
    var SideMenuDataArr = [[JSON]]()
    var isCollapsible = Array<Bool>()
    var indexo = [0,0]
    var menuSelection: ((Array<Int>)->())?
    var mainMenuNameArray = [JSON]()
    var mainMenuChildArray = [JSON]()
    var mainMenuArray = [JSON]()
    var cmsMenuArray = [JSON]()
    var subMenuArray = [JSON]()
    var userDict1 = [String : JSON]()
    var name = String()
    var isOpenBool = false
    //    var optionArray = ["My Orders","My Cart","My Wishlist","My Account","Notifications","Login",]
    
    //MARK:- VIEW_METHODS
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        ApiCallToGetMenuList()
        colSidemenu.register(UINib(nibName: "HeaderCVCell", bundle: nil), forSupplementaryViewOfKind: UICollectionView.elementKindSectionHeader, withReuseIdentifier: "HeaderCVCell")
        colSidemenu.register(UINib(nibName: "MenuCVCell", bundle: nil), forCellWithReuseIdentifier: "MenuCVCell")
        colSidemenu.register(UINib(nibName: "ExtraCollectionViewCell", bundle: nil), forSupplementaryViewOfKind: UICollectionView.elementKindSectionHeader, withReuseIdentifier: "ExtraCollectionViewCell")
        SideMenuDataArr.removeAll()
        SideMenuHeaderArr.removeAll()
        colSidemenu.reloadData()
    }
    
    override func viewDidLayoutSubviews() {
        imgUser.layer.cornerRadius = imgUser.frame.width / 2
    }
    
    override func viewWillAppear(_ animated: Bool) {
        if UserDefaults.standard.value(forKey: "token") != nil {
            ApiCallTogetUserDetails()
 
        }
        else {
            self.lblUsername.text  = "Guest User"
            self.lblMobile.isHidden = true
        }
        
        //self.imgUser.layer.cornerRadius = self.imgUser.frame.height/2
    }
    
    //MARK:- FUNCTIONS
    
    func hideSideMenu() {
        self.view.backgroundColor = .clear
        UIView.animate(withDuration: 0.3, animations: { () -> Void in
            self.view.frame = CGRect(x: 0 - UIScreen.main.bounds.size.width, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
        }, completion: nil)
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        if touches.first!.view == self.view {
            hideSideMenu()
        }
    }
    
    @objc func handleTap(sender: UITapGestureRecognizer) {
        //   DispatchQueue.main.async {
        if sender.view!.tag < self.SideMenuHeaderArr.count - 1 {
            self.isCollapsible[sender.view!.tag] = !self.isCollapsible[sender.view!.tag]
            self.colSidemenu.reloadSections(IndexSet(integer: sender.view!.tag))
            self.indexo[1] = 0
            self.indexo[0] = sender.view!.tag
            // print(self.SideMenuDataArr)
            // self.menuSelection?(self.indexo)
        }
        else {
            self.indexo[1] = 0
            self.indexo[0] = sender.view!.tag
            // self.menuSelection?(self.indexo)
            self.hideSideMenu()
            
        }
        //  }
    }
    
//    func revealSideMenu() {
//        UIApplication.shared.keyWindow?.addSubview(self.view)
//        self.view.backgroundColor = .clear
//        self.view.frame = CGRect(x: 0 - UIScreen.main.bounds.size.width, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
//        UIView.animate(withDuration: 0.3, animations: { () -> Void in
//            self.view.frame = CGRect(x: 0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
//        }, completion: { (Bool) in
//            UIView.animate(withDuration: 0.5) {
//                self.view.backgroundColor = UIColor.black.withAlphaComponent(0.15)
//            }
//        })
//        self.view.layoutIfNeeded()
//
//        if UserDefaults.standard.value(forKey: "token") != nil {
//            ApiCallTogetUserDetails()
//        }
//        else {
//            self.lblUsername.text  = "Guest User"
//        }
//
//
//    }
    func ApiCallTogetUserDetails() {
        getMethodWithAuthorizationReturnJson(apiName: "my-profile/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                self.lblUsername.text = "\(data["first_name"]!.stringValue) \(data["last_name"]!.stringValue)"
                UserDefaults.standard.setValue("\(self.lblUsername.text!)", forKey: "username")
                UserDefaults.standard.synchronize()
                if let mob = data["phone"]?.string {
                      self.lblMobile.text = data["phone"]!.stringValue
                    self.lblMobile.isHidden = false
                }
            }
        }
    }
    
    //MARK:- BUTTON_ACTIONS
    
    @IBAction func signInTapped(_ sender: UIButton) {
        if UserDefaults.standard.value(forKey: "token") != nil {
            hideSideMenu()
            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "ProfileViewController" ) as! ProfileViewController
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
    
    @objc func btnMyordersAction(sender : UIButton) {
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
    @objc func btnMycartAction(sender : UIButton) {
        hideSideMenu()
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
        
        
    }
    @objc func btnMyWishlistAction(sender : UIButton) {
        hideSideMenu()
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
    @objc func btnMyAccountAction(sender : UIButton) {
        hideSideMenu()
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
    @objc func btnMynotificationAction(sender : UIButton) {
        hideSideMenu()
    }
    @objc func btnLoginAction(sender : UIButton) {
        if UserDefaults.standard.value(forKey: "token") != nil {
            UserDefaults.standard.setValue(nil, forKey: "is-login")
            UserDefaults.standard.setValue(nil, forKey: "token")
            UserDefaults.standard.setValue(nil, forKey: "first_name")
            UserDefaults.standard.setValue(nil, forKey: "last_name")
            UserDefaults.standard.removeObject(forKey: "recent_search")
            UserDefaults.standard.synchronize()
            hideSideMenu()
            let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
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
    
    @objc func btnContactUsAction(sender:UIButton) {
        hideSideMenu()
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "ContactUsViewController") as! ContactUsViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
        
    }
    @objc func btnAboutUsAction(sender:UIButton) {
        hideSideMenu()
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "AboutUsViewController") as! AboutUsViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
    }
    @objc func btnVisionAndPurposeAction(sender:UIButton) {
        hideSideMenu()
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "OurVisionAndPurposeViewController") as! OurVisionAndPurposeViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
    }
    @objc func btnQualityStandardAction(sender:UIButton) {
        hideSideMenu()
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "QualityStandardViewController") as! QualityStandardViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
    }
    @objc func btnPrivacyPolicyAction(sender:UIButton) {
        hideSideMenu()
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "PrivacyPolicyViewController") as! PrivacyPolicyViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
    }
    @objc func btnTermsAndConditionAction(sender:UIButton) {
        hideSideMenu()
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let viewController = storyboard.instantiateViewController(withIdentifier: "TermsAndConditionViewController") as! TermsAndConditionViewController
        let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
        navigationController.pushViewController(viewController, animated: true)
    }
    
    
    //MARK:- Api Calling
    func ApiCallToGetMenuList() {
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        let para : [String : Any] = ["warehouse_id": wareHouseId,"lang_code": "en","website_id": 1]
        requestWith(endUrl: "menu_bar/", imageData: nil, parameters: para, onCompletion: { (response) in
            //  print(response!)
            if response!["status"].intValue == 1 {
                //  self.mainMenuArray = response!["menu_bar"].arrayValue
                self.cmsMenuArray = response!["cms_menu"].arrayValue
                
                self.SideMenuHeaderArr = response!["menu_bar"].arrayValue
                self.colSidemenu.register(UINib(nibName: "HeaderCVCell", bundle: nil), forSupplementaryViewOfKind: UICollectionView.elementKindSectionHeader, withReuseIdentifier: "HeaderCVCell")
                self.colSidemenu.register(UINib(nibName: "MenuCVCell", bundle: nil), forCellWithReuseIdentifier: "MenuCVCell")
                for i in 0..<self.SideMenuHeaderArr.count {
                    for ind in 0..<self.SideMenuHeaderArr[i]["child"].arrayValue.count {
                        self.SideMenuDataArr.append(self.SideMenuHeaderArr[ind]["child"].arrayValue)
                    }
                    self.isCollapsible.append(true)
                }
                self.colSidemenu.dataSource = self
                self.colSidemenu.delegate = self
                self.colSidemenu.reloadData()
            }
            else {
                createalert(title: "Alert", message: "Unable to fetch data", vc: self)
            }
        }) { (error) in
        }
    }
    
    
    
}

extension SidemenuController: UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
    
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return SideMenuHeaderArr.count + 1
    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        //        var returnCount = Int()
        if section < SideMenuHeaderArr.count {
            if isCollapsible[section] == true { return 0 }
            else {
                // return SideMenuDataArr.count
                return self.SideMenuHeaderArr[section]["child"].arrayValue.count
                
            }
        }
        else {
            return 1
        }
        
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, referenceSizeForHeaderInSection section: Int) -> CGSize {
        if section < SideMenuHeaderArr.count {
            return CGSize(width: colSidemenu.bounds.width, height: 50)
        }
        else {
            return CGSize(width: colSidemenu.bounds.width, height: 618)
        }
        // return CGSize(width: colSidemenu.bounds.width, height: 50)
    }
    
    func collectionView(_ collectionView: UICollectionView, viewForSupplementaryElementOfKind kind: String, at indexPath: IndexPath) -> UICollectionReusableView {
        // var titleView = UICollectionViewCell()
        
        if indexPath.section < SideMenuHeaderArr.count{
            let headerView = colSidemenu.dequeueReusableSupplementaryView(ofKind: UICollectionView.elementKindSectionHeader, withReuseIdentifier: "HeaderCVCell", for: indexPath) as! HeaderCVCell
            
            
            let headerTap = UITapGestureRecognizer(target: self, action: #selector(handleTap(sender:)))
            headerView.tag = indexPath.section
            headerView.addGestureRecognizer(headerTap)
            headerView.lblTitle.text = SideMenuHeaderArr[indexPath.section]["name"].stringValue
            headerView.imgArrow.isHidden = true
            headerView.lblTitle.textColor = UIColor.black
            if SideMenuDataArr[indexPath.section][indexPath.row].arrayValue.count != 0 {
                headerView.imgArrow.isHidden = false
                if isCollapsible[indexPath.section] {
                    UIView.animate(withDuration: 1) {
                        headerView.imgArrow.transform = CGAffineTransform.identity
                    }
                    headerView.lblTitle.textColor = UIColor.black
                } else {
                    UIView.animate(withDuration: 1) {
                        headerView.imgArrow.transform = CGAffineTransform(rotationAngle: .pi)
                        
                    }
                    headerView.lblTitle.textColor = .lightGray
                }
            }
            return headerView
        }
        else {
            let extraView = colSidemenu.dequeueReusableSupplementaryView(ofKind: UICollectionView.elementKindSectionHeader, withReuseIdentifier: "ExtraCollectionViewCell", for: indexPath) as! ExtraCollectionViewCell
            let headerTap = UITapGestureRecognizer(target: self, action: #selector(handleTap(sender:)))
            extraView.tag = indexPath.section
            extraView.addGestureRecognizer(headerTap)
            
            extraView.btnMyOrders.tag = indexPath.section
            extraView.btnMyOrders.addTarget(self, action: #selector(btnMyordersAction), for: .touchUpInside)
            
            extraView.btnMyCart.tag = indexPath.section
            extraView.btnMyCart.addTarget(self, action: #selector(btnMycartAction), for: .touchUpInside)
            
            extraView.btnMyWishList.tag = indexPath.section
            extraView.btnMyWishList.addTarget(self, action: #selector(btnMyWishlistAction), for: .touchUpInside)
            
            extraView.btnMyAccount.tag = indexPath.section
            extraView.btnMyAccount.addTarget(self, action: #selector(btnMyAccountAction), for: .touchUpInside)
            
            extraView.btnNotifications.tag = indexPath.section
            extraView.btnNotifications.addTarget(self, action: #selector(btnMynotificationAction), for: .touchUpInside)
            
            extraView.btnContactUs.tag = indexPath.section
            extraView.btnContactUs.addTarget(self, action: #selector(btnContactUsAction), for: .touchUpInside)
            
            extraView.btnAboutUs.tag = indexPath.section
            extraView.btnAboutUs.addTarget(self, action: #selector(btnAboutUsAction), for: .touchUpInside)
            
            extraView.btnVisionAndPurpose.tag = indexPath.section
            extraView.btnVisionAndPurpose.addTarget(self, action: #selector(btnVisionAndPurposeAction), for: .touchUpInside)
            
            extraView.btnQualityStandard.tag = indexPath.section
            extraView.btnQualityStandard.addTarget(self, action: #selector(btnQualityStandardAction), for: .touchUpInside)
            
            
            extraView.btnPrivacyPolicy.tag = indexPath.section
            extraView.btnPrivacyPolicy.addTarget(self, action: #selector(btnPrivacyPolicyAction), for: .touchUpInside)
            
            extraView.btnTermsAndCondition.tag = indexPath.section
            extraView.btnTermsAndCondition.addTarget(self, action: #selector(btnTermsAndConditionAction), for: .touchUpInside)
            
             if UserDefaults.standard.value(forKey: "token") != nil {
                extraView.lblLogin.text = "Logout"
                extraView.btnLogin.tag = indexPath.section
                extraView.btnLogin.addTarget(self, action: #selector(btnLoginAction), for: .touchUpInside)
            }
             else {
                extraView.lblLogin.text = "Login"
                extraView.btnLogin.tag = indexPath.section
                extraView.btnLogin.addTarget(self, action: #selector(btnLoginAction), for: .touchUpInside)
            }
            return extraView
        }
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = colSidemenu.dequeueReusableCell(withReuseIdentifier: "MenuCVCell", for: indexPath) as! MenuCVCell
        if indexPath.section < SideMenuHeaderArr.count {
              cell.lblTitle.text = SideMenuHeaderArr[indexPath.section]["child"][indexPath.row]["name"].stringValue
        }
        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        indexo[1] = indexPath.row
        if SideMenuHeaderArr[indexo[0]]["child"][indexo[1]].dictionaryValue.isEmpty == false {
            let childDict = SideMenuHeaderArr[indexo[0]]["child"][indexo[1]].dictionaryValue
                 print(childDict)
                 let slug = childDict["slug"]!.stringValue
                 let title = childDict["name"]!.stringValue
                 print(slug)
                 hideSideMenu()
                 let slugDict : [String:Any] = ["slug": slug, "title": title]
                 print(slugDict)
                 let storyboard : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                 let vc : ProductListingViewController = storyboard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
                 vc.slugDictInListing = slugDict
                 vc.productTitle = title
                 vc.slugInListing = slug
                 vc.sideMenuBool = true
                 vc.navigationType = "present"
                 let navigationController = UINavigationController(rootViewController: vc)
                 navigationController.modalPresentationStyle = UIModalPresentationStyle.fullScreen
                 self.present(navigationController, animated: true, completion: nil)
                 hideSideMenu()
        }
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 0
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 0
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, insetForSectionAt section: Int) -> UIEdgeInsets {
        return UIEdgeInsets(top: 0, left: 0, bottom: 0, right: 0)
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: colSidemenu.bounds.size.width, height: 50.0)
    }
    
}


