//
//  SelectCityViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 18/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
import SDWebImage
class SelectCityViewController: UIViewController ,UICollectionViewDelegate, UICollectionViewDataSource, UIScrollViewDelegate, UICollectionViewDelegateFlowLayout{
    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var collectionView: UICollectionView!
    private let spacing:CGFloat = 8
    var slat = String()
    var slong = String()
    var dataArray = [JSON]()
    var screenSize: CGRect!
    var screenWidth: CGFloat!
    var screenHeight: CGFloat!
    var selectedIndex  = Int()
    var storeID = String()
    override func viewDidLoad() {
        super.viewDidLoad()
        
        screenSize = UIScreen.main.bounds
        screenWidth = screenSize.width
        screenHeight = screenSize.height
        navigationView.addShadow1()
        ApiCallToSetLocation()
        let layout: UICollectionViewFlowLayout = UICollectionViewFlowLayout()
        layout.sectionInset = UIEdgeInsets(top: 0, left: 0, bottom: 0, right: 0)
        layout.itemSize = CGSize(width: screenWidth/2, height: screenWidth/2)
        layout.minimumInteritemSpacing = 15
        layout.minimumLineSpacing = 15
        collectionView!.collectionViewLayout = layout
    }
    override func viewWillAppear(_ animated: Bool) {
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.isNavigationBarHidden = true
    }
    @IBAction func btnBackAction(_ sender: Any) {
        let vc = storyboard?.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return dataArray.count
     //    return 15
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "CityCollectionViewCell", for: indexPath) as! CityCollectionViewCell
     //   cell.imgCity.layer.cornerRadius = cell.imgCity.frame.height/2
      //  cell.imgCity.layer.cornerRadius = 5
        cell.cellView.layer.cornerRadius = 5
        cell.cellView.addShadow1()
        cell.cellView.layer.borderColor = UIColor.lightGray.cgColor
        cell.cellView.layer.borderWidth = 0.5
        
        let dataDict = dataArray[indexPath.row].dictionaryValue
   //     cell.lblCity.text = dataDict["name"]?.stringValue
        if  dataDict["warehouse_logo"]?.stringValue != nil {
            let storePic = dataDict["warehouse_logo"]?.stringValue
            let fullUrl = WAREHOUSE_LOGO + storePic!
            let url = URL(string: fullUrl)
            print(url!)
          //  cell.imgCity.sd_setImage(with: url!)
            cell.imgCity.sd_setImage(with: url, placeholderImage: UIImage(named: "no_image"))
        }
//        else {
//            cell.imgCity.image = UIImage(named: "no_image")
//        }
         cell.imgCity.layer.cornerRadius = 5
        // bannerCell.bannerView.addShadow1()
        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        let dataDict = dataArray[indexPath.row].dictionaryValue
        print(dataDict)
        
        if let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as? Int {
            let wareHouseID = dataDict["id"]!.intValue
            if wareHouseId != wareHouseID {
                self.ApiCallToGetCartCount(index : indexPath.row)
//                SetUpWareHouseView()
//                selectedIndex = indexPath.row
                
            }
            else {
                let mainStoryBoard = UIStoryboard(name: "Home", bundle: nil)
                let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                let wareHouseName = dataDict["name"]!.stringValue
                let wareHouseID = dataDict["id"]!.intValue
                print(wareHouseName)
                print(wareHouseID)
                UserDefaults.standard.setValue(wareHouseName, forKey: "WareHouseName")
                UserDefaults.standard.set(wareHouseID, forKey: "WareHouseId")
                UserDefaults.standard.synchronize()
                print(UserDefaults.standard.value(forKey: "WareHouseId")!)
                self.navigationController?.pushViewController(redViewController, animated: true)
            }
        }
        else {
            let mainStoryBoard = UIStoryboard(name: "Home", bundle: nil)
            let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
            let wareHouseName = dataDict["name"]!.stringValue
            let wareHouseID = dataDict["id"]!.intValue
            print(wareHouseName)
            print(wareHouseID)
            UserDefaults.standard.setValue(wareHouseName, forKey: "WareHouseName")
            UserDefaults.standard.set(wareHouseID, forKey: "WareHouseId")
            UserDefaults.standard.synchronize()
            print(UserDefaults.standard.value(forKey: "WareHouseId")!)
            self.navigationController?.pushViewController(redViewController, animated: true)
        }
        
    }
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        
        let noOfCellsInRow = 1
        let flowLayout = collectionViewLayout as! UICollectionViewFlowLayout
        let totalSpace = flowLayout.sectionInset.left
            + flowLayout.sectionInset.right
            + (flowLayout.minimumInteritemSpacing * CGFloat(noOfCellsInRow - 1))
        let size = Int((collectionView.bounds.width - totalSpace) / CGFloat(noOfCellsInRow))
        return CGSize(width: size, height: 120)
    }
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, insetForSectionAt section: Int) -> UIEdgeInsets {
        return UIEdgeInsets.zero
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 8
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 8
    }
    
    func SetUpWareHouseView() {
        requestWareHouseView(vc: self)
        wareHouseXib.btnNo.addTarget(self, action: #selector(btnNoAction), for: .touchUpInside)
        wareHouseXib.btnYes.addTarget(self, action: #selector(btnYesAction), for: .touchUpInside)
        
        wareHouseXib.viewWareHouse.layer.shadowColor = UIColor.lightGray.cgColor
        wareHouseXib.viewWareHouse.layer.shadowOpacity = 1
        wareHouseXib.viewWareHouse.layer.shadowOffset = .zero
        wareHouseXib.viewWareHouse.layer.cornerRadius = 5
        wareHouseXib.viewWareHouse.layer.shadowRadius = 1
        wareHouseXib.viewWareHouse.layer.shadowPath = UIBezierPath(rect: wareHouseXib.viewWareHouse.bounds).cgPath
        wareHouseXib.viewWareHouse.layer.shouldRasterize = true
        wareHouseXib.viewWareHouse.layer.rasterizationScale = UIScreen.main.scale
        
    }
    
    @objc func btnYesAction() {
        ApiCallToEmptyCart()
    }
    @objc func btnNoAction() {
        wareHouseXib.removeFromSuperview()
    }
    
    //    MARK:- Api Calling
    func ApiCallToSetLocation() {
        let para: [String:Any] = ["latitude":self.slat,"longitude":self.slong,"website_id":"1","storetype_id":storeID]
     //   let para: [String:Any] = ["latitude":"22.572646","longitude":"88.36389500000001","website_id":"1" ,"storetype_id":"16"]
        postMethodReturnJson(apiName: "warehouse-list/", params: para, vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                self.dataArray = response["data"].arrayValue
                self.collectionView.delegate = self
                self.collectionView.dataSource = self
                self.collectionView.reloadData()
            }
            else {
                requestNoWareHouseView(vc: self)
                NowareHouseXib.viewWareHouse.layer.shadowColor = UIColor.lightGray.cgColor
                NowareHouseXib.viewWareHouse.layer.shadowOpacity = 1
                NowareHouseXib.viewWareHouse.layer.shadowOffset = .zero
                NowareHouseXib.viewWareHouse.layer.cornerRadius = 5
                NowareHouseXib.viewWareHouse.layer.shadowRadius = 1
                NowareHouseXib.viewWareHouse.layer.shadowPath = UIBezierPath(rect: NowareHouseXib.viewWareHouse.bounds).cgPath
                NowareHouseXib.viewWareHouse.layer.shouldRasterize = true
                NowareHouseXib.viewWareHouse.layer.rasterizationScale = UIScreen.main.scale
                NowareHouseXib.btnChaneLocation.addTarget(self,action:#selector(self.btnChangeLocationAction) , for: .touchUpInside)
                NowareHouseXib.btnChaneLocation.layer.borderColor = UIColor.white.cgColor
                NowareHouseXib.btnChaneLocation.layer.borderWidth = 0.5
                NowareHouseXib.btnChaneLocation.layer.cornerRadius = 5
            }
        }
    }
    @objc func btnChangeLocationAction() {
    NowareHouseXib.removeFromSuperview()
    self.navigationController?.popViewController(animated: true)
//    let vc = storyboard?.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
//    self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func ApiCallToEmptyCart() {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            let para:[String:Any] = ["website_id":"1" , "device_id":deviceID]
            postMethodReturnWithAuthorizationJson(apiName: "empty-cart/", params: para, vc: self) { (response : JSON) in
                print(response)
                if response["status"].intValue == 200 {
                    let dataDict = self.dataArray[self.selectedIndex].dictionaryValue
                    print(dataDict)
                    let wareHouseName = dataDict["name"]!.stringValue
                    let wareHouseID = dataDict["id"]!.intValue
                    print(wareHouseName)
                    print(wareHouseID)
                    UserDefaults.standard.setValue(wareHouseName, forKey: "WareHouseName")
                    UserDefaults.standard.set(wareHouseID, forKey: "WareHouseId")
                    UserDefaults.standard.synchronize()
                    DataBaseHelper.sharedInstance.deleteAllRecords()
                    wareHouseXib.removeFromSuperview()
                    let mainStoryBoard = UIStoryboard(name: "Home", bundle: nil)
                    let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                    self.navigationController?.pushViewController(redViewController, animated: true)
                    
                }
            }
        }
        else {
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            let para:[String:Any] = ["website_id":"1" , "device_id":deviceID]
            postMethodReturnJson(apiName: "empty-cart/", params: para, vc: self) { (response : JSON) in
                print(response)
                if response["status"].intValue == 200 {
                    let dataDict = self.dataArray[self.selectedIndex].dictionaryValue
                    print(dataDict)
                    let wareHouseName = dataDict["name"]!.stringValue
                    let wareHouseID = dataDict["id"]!.intValue
                    print(wareHouseName)
                    print(wareHouseID)
                    UserDefaults.standard.setValue(wareHouseName, forKey: "WareHouseName")
                    UserDefaults.standard.set(wareHouseID, forKey: "WareHouseId")
                    UserDefaults.standard.synchronize()
                    DataBaseHelper.sharedInstance.deleteAllRecords()
                    wareHouseXib.removeFromSuperview()
                    let mainStoryBoard = UIStoryboard(name: "Home", bundle: nil)
                    let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                    self.navigationController?.pushViewController(redViewController, animated: true)
                }
            }
        }
    }
    
    
    func ApiCallToGetCartCount(index : Int){
        var auth : String?
        var deviceId : String
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
         let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
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
                    self.SetUpWareHouseView()
                    self.selectedIndex = index
                  //  self.ApiCallToEmptyCart()

                   // self.ApiCallToViewCart()
                }
                else {
                    let dataDict = self.dataArray[index].dictionaryValue
                    print(dataDict)
                    let mainStoryBoard = UIStoryboard(name: "Home", bundle: nil)
                    let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                    let wareHouseName = dataDict["name"]!.stringValue
                    let wareHouseID = dataDict["id"]!.intValue
                    print(wareHouseName)
                    print(wareHouseID)
                    UserDefaults.standard.setValue(wareHouseName, forKey: "WareHouseName")
                    UserDefaults.standard.set(wareHouseID, forKey: "WareHouseId")
                    UserDefaults.standard.synchronize()
                    print(UserDefaults.standard.value(forKey: "WareHouseId")!)
                    self.navigationController?.pushViewController(redViewController, animated: true)
//                    self.btnCartCount.isHidden = true
//                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
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
                    self.SetUpWareHouseView()
                    self.selectedIndex = index

                   // self.ApiCallToViewCart()
                }
                else {
                    let dataDict = self.dataArray[index].dictionaryValue
                    print(dataDict)
                    let mainStoryBoard = UIStoryboard(name: "Home", bundle: nil)
                    let redViewController = mainStoryBoard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                    let wareHouseName = dataDict["name"]!.stringValue
                    let wareHouseID = dataDict["id"]!.intValue
                    print(wareHouseName)
                    print(wareHouseID)
                    UserDefaults.standard.setValue(wareHouseName, forKey: "WareHouseName")
                    UserDefaults.standard.set(wareHouseID, forKey: "WareHouseId")
                    UserDefaults.standard.synchronize()
                    print(UserDefaults.standard.value(forKey: "WareHouseId")!)
                    self.navigationController?.pushViewController(redViewController, animated: true)

//                    self.btnCartCount.isHidden = true
//                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                }
                
            }
        }
    }
    
}
extension UIView {
    func addShadow1() {
        self.layer.shadowColor = UIColor.lightGray.cgColor
        self.layer.shadowOffset = CGSize(width: 0, height: 1)
        self.layer.shadowOpacity = 1
        self.layer.shadowRadius = 1.5
        self.clipsToBounds = false
    }
    func addShadowNote() {
         self.layer.shadowColor = UIColor.lightGray.cgColor
         self.layer.shadowOffset = CGSize(width: 0, height: 1)
         self.layer.shadowOpacity = 1
         self.layer.shadowRadius = 1
         self.clipsToBounds = false
     }
}

