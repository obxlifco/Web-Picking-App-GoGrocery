//
//  SubstituteViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 26/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class SubstituteViewController: UIViewController , UIScrollViewDelegate{
    
    @IBOutlet weak var viewQuitAlpha: UIView!
    @IBOutlet weak var btnNo: UIButton!
    @IBOutlet weak var btnYes: UIButton!
    @IBOutlet weak var viewYesNo: UIView!
    @IBOutlet weak var viewQuit: UIView!
    @IBOutlet weak var mainCollectionView: UICollectionView!
    @IBOutlet weak var lblTitle: UILabel!
    @IBOutlet weak var btnSubmitReplacement: UIButton!
    @IBOutlet weak var btndontReplacement: UIButton!
    @IBOutlet weak var lblTimeRemaining: UILabel!
    @IBOutlet weak var btnBack: UIButton!
    private let spacing:CGFloat = 0
    var scrollCount = 1
    var mainArrayCount = 5
    var timerCount = 600
    var orderId = 0// order id
    weak var timer: Timer?
    var productsArray = [JSON]()
    var substituteArray = [JSON]()
    var idArray = [Int]()
    var countArray = [Int]()
    var tempMainDict = [String:Any]()
   // var cartDatafromDb = [AddcCart]()
    var defaultIndex = 0
    var approvalArray = [[String:Any]]()
    var tempCartArray = [[String:Any]]()
    var maxQuantityForIndex = Int()
    var localCartArray = [[String:Any]]()
    var mainCollectionIndex = 0
    var substituteSubmitted = [Int]()
    var submittedPosition = [Bool]()
    var cartInAction = false
    var maxQuantityCheck = 0
    var childCollectionHeight = 270
    
    
    //MARK: - Class lifeCycle
    //MARK: -
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        mainCollectionView.dataSource = self
        mainCollectionView.delegate = self
        mainCollectionView.isPagingEnabled = true
        self.ApiCallToGetSubstituteProduct()
        
    }
    override func viewWillAppear(_ animated: Bool) {
        approvalArray.removeAll()
        self.navigationController?.isNavigationBarHidden = true
    }
    override func viewDidDisappear(_ animated: Bool) {
        stopTimer()
    }
    //MARK: -
    //MARK: -
    
    //MARK: - Convert UTC to Local time
    func utcToLocal(dateStr: String) -> String? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        dateFormatter.timeZone = TimeZone(abbreviation: "UTC")
        dateFormatter.locale = Locale(identifier: "en")
        if let date = dateFormatter.date(from: dateStr) {
            dateFormatter.timeZone = TimeZone.current
            dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        
            return dateFormatter.string(from: date)
        }
        return nil
    }
    //MARK: - Timer Functionality
    //MARK: -
    func startTimer() {
        timer?.invalidate()   // just in case you had existing `Timer`, `invalidate` it before we lose our reference to it
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            if(self!.timerCount > 0){
                let minutes = String((self!.timerCount) / 60)
                let seconds = (self!.timerCount) % 60
                var secondIntString = String(seconds)
                if seconds < 10 {
                  secondIntString = "0\(seconds)"
                }
                self!.lblTimeRemaining.text = "Time Remaining \(minutes) : \(secondIntString)"
                self?.timerCount = (self!.timerCount) - 1
                //print("time \(minutes) : \(seconds)")
            } else {
                self!.timer?.invalidate()
                let alertController = UIAlertController(title: "Alert", message: "Your Session for substitute product has been expired", preferredStyle:.alert)

                alertController.addAction(UIAlertAction(title: "OK", style: .default)
                { action -> Void in
                    self!.ApiCallToPickerNotification()
                })
                self?.present(alertController, animated: true, completion: nil)
            }
        }
    }
    
    func stopTimer() {
        timer?.invalidate()
    }
    //MARK: -
    //MARK: -
    
    //MARK: - Quit view
    func SetUpQuitView () {
        viewQuit.layer.cornerRadius = 5
        viewQuit.addShadow1()
        btnYes.layer.cornerRadius = 5
        btnNo.layer.cornerRadius = 5
        viewYesNo.layer.cornerRadius = 5
        viewYesNo.addShadow1()
        UIView.animate(withDuration: 0.5,
                       animations: { [weak self] in
                        self?.viewQuit.alpha = 1
                        self?.viewQuitAlpha.alpha = 1
        })
    }
    
    //    MARK:- Button Actions
    @IBAction func btnBackAction(_ sender: Any) {
        if self.defaultIndex == 0 {
            SetUpQuitView ()
        }
        else {
            tempCartArray = approvalArray
            if tempCartArray.count != 0 {
                tempCartArray.removeAll()
                let alert = UIAlertController(title: "Alert", message: "There are items added in the list, please submit replacement", preferredStyle: .alert)
                alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            } else {
                self.lblTitle.text = "Missing item \(defaultIndex) of \(self.productsArray.count)"
                defaultIndex = self.defaultIndex - 1
                maxQuantityCheck = 0
                self.mainCollectionView.reloadData()
                mainCollectionView.scrollToPreviousItem()
                DispatchQueue.main.async {
                    if self.defaultIndex != 0 {
                        self.btnBack.setImage(UIImage(named: "back_black"), for: .normal)
                    } else {
                        self.btnBack.setImage(UIImage(named: "cancel_black"), for: .normal)
                    }
                }
            }
            
            
        }
    }
    @IBAction func btnSubmitReplacement(_ sender: Any) {
        let mainDict = self.productsArray[defaultIndex].dictionaryValue
        let mainproductId = mainDict["id"]!.intValue
        let maxQuantity = mainDict["shortage"]?.intValue ?? 0
        print("submitted \(substituteSubmitted)")
        if self.substituteSubmitted.contains(mainproductId) {
            createalert(title: "Alert", message: "You have alrady submitted your choice for this product", vc: self)
            
        } else {
            if approvalArray.count != 0 {
                if maxQuantityCheck < maxQuantity {
                    let alertController = UIAlertController(title: "Alert", message: "You can add \(maxQuantity-maxQuantityCheck) more quantity Do you still want to submit ?", preferredStyle:.alert)

                    alertController.addAction(UIAlertAction(title: "Yes", style: .default)
                    { action -> Void in
                        self.ApiCallToSubmitReplacementProduct()
                    })
                    alertController.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
                    self.present(alertController, animated: true, completion: nil)
                } else {
                   ApiCallToSubmitReplacementProduct()
                }
                
            }
            else {
                createalert(title: "Alert", message: "Please Add Item for substitute Product", vc: self)
            }
              
        }

    }
    
    @IBAction func btnIDontWantReplacement(_ sender: Any) {
        let mainDict = self.productsArray[defaultIndex].dictionaryValue
        let mainproductId = mainDict["id"]!.intValue
        print("submitted \(substituteSubmitted)")
        if self.substituteSubmitted.contains(mainproductId) {
            createalert(title: "Alert", message: "You have alrady submitted your choice for this product", vc: self)
            
        } else {
            let alertController = UIAlertController(title: "Alert", message: "Do you really want to submit without substitute product ?", preferredStyle:.alert)

            alertController.addAction(UIAlertAction(title: "Yes", style: .default)
            { action -> Void in
                self.ApiCallToSubmitReplacementProduct(isNoSubstitute: true)
            })
            alertController.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
            self.present(alertController, animated: true, completion: nil)
            
        }
        
    }
    
    @IBAction func btnYesAction(_ sender: Any) {
        UIView.animate(withDuration: 0.5,
                       animations: { [weak self] in
                        self?.viewQuit.alpha = 0
                        self?.viewQuitAlpha.alpha = 0
        })
        self.ApiCallToResetOrder()
        
    }
    
    @IBAction func btnNoAction(_ sender: Any) {
        UIView.animate(withDuration: 0.5,
                       animations: { [weak self] in
                        self?.viewQuit.alpha = 0
                        self?.viewQuitAlpha.alpha = 0
        })
    }
    
    
    //    MARK:- Add to cart Functionality
    @objc func addToCartbtnAction(sender: UIButton) {
        guard cartInAction == false else { //Check if all process of plus action completed before user tapp again
            return
        }
        cartInAction = true
        var count = 0
     //   self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        let cell: MainCollectionViewCell? = (mainCollectionView.cellForItem(at: IndexPath.init(row: defaultIndex, section: 0)) as! MainCollectionViewCell)
        let cell1: SubstituteCollectionViewCell? = (cell?.subsCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! SubstituteCollectionViewCell)
       
        let mainDict = self.productsArray[defaultIndex].dictionaryValue
        let productDict  = mainDict["product"]?.dictionaryValue
        let productId = productDict!["id"]!.intValue
        let substititArr = mainDict["substitute_products"]!.arrayValue
        let substititDict = substititArr[sender.tag].dictionaryValue
        let maxQuantity = mainDict["shortage"]?.intValue
        
        let subsProductDict  = substititDict["product"]?.dictionaryValue
        let quantity1 = substititDict["quantity"]?.intValue
        let subsProductID = subsProductDict!["id"]!.intValue
        
        let orderProductId = substititDict["id"]!.intValue
        print(subsProductID)
         print(productId)
        
        print(sender.tag)
        print(defaultIndex)
        guard maxQuantityCheck < maxQuantity! else { // Check if user has choose all sortage quantity
            cartInAction = false
            createalert(title: "Alert", message: "Your can choose upto \(maxQuantity!) quantity for substitute", vc: self)
            return
        }
        maxQuantityCheck = maxQuantityCheck + 1
        count = count + 1
        
        cell1!.btnAddtoCart.setTitle("\(count)", for: .normal)
        cell1!.btnPlus.isHidden = false
        cell1!.btnMinus.isHidden = false
        cell1!.btnAddtoCart.backgroundColor = .white
        cell1!.btnAddtoCart.setTitleColor(.black, for: .normal)
        cell1!.cartStack.layer.cornerRadius = 5
        cell1!.cartStack.clipsToBounds = true
        cell1!.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        cell1!.cartStack.layer.borderWidth = 1
     //   let dict = ["cost":"0" ,"product_id":"\(subsProductID)","quantity":"\(count)"] as [String : Any]
      //  DataBaseHelper.sharedInstance.save(object: dict)
      //  print(DataBaseHelper.sharedInstance.getCartData())
        for (index, element) in approvalArray.enumerated() {
              if "\(subsProductID)" == "\(element["substitute_product_id"] as! Int)"{
                  if self.approvalArray.count > index {
                      self.approvalArray.remove(at: index)
                  }
                 
                 }
             }
        
          for (index, element) in localCartArray.enumerated() {
                     if "\(subsProductID)" == "\(element["product_id"] as! String)"{
                      if self.localCartArray.count > index {
                          self.localCartArray.remove(at: index)
                      }
                         
                        }
          }

        
        let approvalDict:[String:Any] = ["product_id":productId,"substitute_product_id":subsProductID,"order_product_id":orderProductId,"quantity":quantity1!,"grn_quantity":count]
        self.approvalArray.append(approvalDict)
        self.tempCartArray.append(approvalDict)
        let dictCart = ["product_id":"\(subsProductID)","quantity":"\(count)","main_product_id":"\(productId)"] as [String : Any]
        localCartArray.append(dictCart)
        print(localCartArray)
        cartInAction = false
        
    }
    
    @objc func btnPlusAction(sender: UIButton) {
        guard cartInAction == false else { //Check if all process of plus action completed before user tapp again
            return
        }
        cartInAction = true
        var newQuantity = Int()
        
//        self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        let cell: MainCollectionViewCell? = (mainCollectionView.cellForItem(at: IndexPath.init(row: defaultIndex, section: 0)) as! MainCollectionViewCell)
        let cell1: SubstituteCollectionViewCell? = (cell?.subsCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! SubstituteCollectionViewCell)
        
        let mainDict = self.productsArray[defaultIndex].dictionaryValue
        let productDict  = mainDict["product"]?.dictionaryValue
        let productId = productDict!["id"]!.intValue
        let substititArr = mainDict["substitute_products"]!.arrayValue
        let substititDict = substititArr[sender.tag].dictionaryValue
        let maxQuantity = mainDict["shortage"]?.intValue
        let subsProductDict  = substititDict["product"]?.dictionaryValue
        let quantity1 = substititDict["quantity"]?.intValue
        let subsProductID = subsProductDict!["id"]!.intValue
        let orderProductId = substititDict["id"]!.intValue
        print(subsProductID)
         print(productId)
        guard maxQuantityCheck < maxQuantity! else { // Check if user has choose all sortage quantity
            cartInAction = false
            createalert(title: "Alert", message: "Your can choose upto \(maxQuantity!) quantity for substitute", vc: self)
            return
        }
        maxQuantityCheck = maxQuantityCheck + 1

        for (_, element) in localCartArray.enumerated() {
            if "\(subsProductID)" == element["product_id"] as! String {
                let quantt = element["quantity"] as! String
                var inttype: Int = Int(quantt)!
                print(inttype)
                inttype = inttype + 1
                newQuantity = inttype
            }
        }
        cell1!.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
        cell1!.btnPlus.isHidden = false
        cell1!.btnMinus.isHidden = false
        cell1!.btnAddtoCart.backgroundColor = .white
        cell1!.btnAddtoCart.setTitleColor(.black, for: .normal)
        cell1!.cartStack.layer.cornerRadius = 5
        cell1!.cartStack.clipsToBounds = true
        cell1!.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        cell1!.cartStack.layer.borderWidth = 1
       // let dict = ["cost":"0" ,"product_id":"\(subsProductID)","quantity":"\(newQuantity)"] as [String : Any]
       // DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
            for (index, element) in approvalArray.enumerated() {
                if "\(subsProductID)" == "\(element["substitute_product_id"] as! Int)"{
                    self.approvalArray.remove(at: index)
                    let approvalDict:[String:Any] = ["product_id":productId,"substitute_product_id":subsProductID,"order_product_id":orderProductId,"quantity":quantity1!,"grn_quantity":newQuantity]
                    self.approvalArray.append(approvalDict as [String : Any])
                   }
               }

        for (index, element) in localCartArray.enumerated() {
            if "\(subsProductID)" == "\(element["product_id"] as! String)"{
                
                self.localCartArray.remove(at: index)
                let dictCart = ["product_id":"\(subsProductID)","quantity":"\(newQuantity)","main_product_id":"\(productId)"] as [String : Any]
                self.localCartArray.append(dictCart as [String : Any])
               }
           }
          print(localCartArray)
        cartInAction = false
      
    }
    @objc func btnMinusAction(sender: UIButton) {
        guard cartInAction == false else {
            return
        }
        cartInAction = true
        var newQuantity = Int()
        //var newProductId = String()
      //    self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        let cell: MainCollectionViewCell? = (mainCollectionView.cellForItem(at: IndexPath.init(row: defaultIndex, section: 0)) as! MainCollectionViewCell)
        let cell1: SubstituteCollectionViewCell? = (cell?.subsCollectionView.cellForItem(at: IndexPath.init(row: sender.tag, section: 0)) as! SubstituteCollectionViewCell)
        
        let mainDict = self.productsArray[defaultIndex].dictionaryValue
        let productDict  = mainDict["product"]?.dictionaryValue
        let productId = productDict!["id"]!.intValue
        
        let substititArr = mainDict["substitute_products"]!.arrayValue
        let substititDict = substititArr[sender.tag].dictionaryValue
        let maxQuantity = mainDict["shortage"]?.intValue
        let subsProductDict  = substititDict["product"]?.dictionaryValue
        let quantity1 = substititDict["quantity"]?.intValue
        let subsProductID = subsProductDict!["id"]!.intValue
        let orderProductId = substititDict["id"]!.intValue
        print(subsProductID)
         
         maxQuantityCheck = maxQuantityCheck - 1
       
        
        
        for (_, element) in localCartArray.enumerated() {
            if "\(subsProductID)" == element["product_id"] as! String {
                let quantt = element["quantity"] as! String
                var inttype: Int = Int(quantt)!
                print(inttype)
                inttype = inttype - 1
                newQuantity = inttype
            }
        }
      
        if newQuantity == 0 {
            // cartAdded = false
         //   DataBaseHelper.sharedInstance.delete(index: coreDataindex)
           // print(DataBaseHelper.sharedInstance.getCartData())
            cell1!.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
            cell1!.btnPlus.isHidden = true
            cell1!.btnMinus.isHidden = true
            cell1!.btnAddtoCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
            cell1!.btnAddtoCart.setTitleColor(.white, for: .normal)
            cell1!.cartStack.layer.cornerRadius = 5
            cell1!.cartStack.clipsToBounds = true
            cell1!.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
            cell1!.cartStack.layer.borderWidth = 1
            for (index, element) in approvalArray.enumerated() {
                if "\(subsProductID)" == "\(element["substitute_product_id"] as! Int)"{
                    if self.approvalArray.count > index {
                        self.approvalArray.remove(at: index)
                    }
                   
                   }
               }
          
            for (index, element) in localCartArray.enumerated() {
                       if "\(subsProductID)" == "\(element["product_id"] as! String)"{
                        if self.localCartArray.count > index {
                            self.localCartArray.remove(at: index)
                        }
                           
                          }
            }
              print(localCartArray)
            
        }
        else {
            cell1!.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
            cell1!.btnPlus.isHidden = false
            cell1!.btnMinus.isHidden = false
            cell1!.btnAddtoCart.backgroundColor = .white
            cell1!.btnAddtoCart.setTitleColor(.black, for: .normal)
            cell1!.cartStack.layer.cornerRadius = 5
            cell1!.cartStack.clipsToBounds = true
            cell1!.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
            cell1!.cartStack.layer.borderWidth = 1
          //  let dict = ["cost":"0" ,"product_id":"\(subsProductID)","quantity":"\(newQuantity)"] as [String : Any]
           // DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
          //  print(DataBaseHelper.sharedInstance.getCartData())
            
            for (index, element) in approvalArray.enumerated() {
                if "\(subsProductID)" == "\(element["substitute_product_id"] as! Int)"{
              self.approvalArray.remove(at: index)
                    let approvalDict:[String:Any] = ["product_id":productId,"substitute_product_id":subsProductID,"order_product_id":orderProductId,"quantity":quantity1!,"grn_quantity":newQuantity]
                    self.approvalArray.append(approvalDict as [String : Any])
               }
              }
            
            for (index, element) in localCartArray.enumerated() {
                if "\(subsProductID)" == "\(element["product_id"] as! String)"{
                    self.localCartArray.remove(at: index)
                    let dictCart = ["product_id":"\(subsProductID)","quantity":"\(newQuantity)","main_product_id":"\(productId)"] as [String : Any]
                    self.localCartArray.append(dictCart as [String : Any])
               }
              }
              print(localCartArray)
            
        }
        cartInAction = false
        
    }
    //MARK: - Scrollview Delegets
    //MARK: -
    func scrollViewDidEndDecelerating(_ scrollView: UIScrollView) {
        guard Int(scrollView.frame.height) != self.childCollectionHeight else {
            return
        }
        tempCartArray = approvalArray
        let center = CGPoint(x: scrollView.contentOffset.x + (scrollView.frame.width / 2), y: (scrollView.frame.height / 2))
        if let ip = mainCollectionView.indexPathForItem(at: center) {
            print("ip")
            print(ip.row)
            print(defaultIndex)
            if defaultIndex != ip.row {
                if tempCartArray.count != 0 {
                    var isFrontBack = Bool()
                    if ip.row < defaultIndex {
                        isFrontBack = true // for front navigation
                    }
                    else {
                        isFrontBack = false // for back navigation
                    }
                    tempCartArray.removeAll()
                    showAlertItemAddedCartScroll(message: "There are items added in the list, please submit replacement", isFrontOrBackBool: isFrontBack)
                }
                else {
                    self.lblTitle.text = "Missing item \(ip.row + 1) of \(self.productsArray.count)"
                    maxQuantityCheck = 0
                    defaultIndex = ip.row
                    self.mainCollectionView.reloadData()
                    DispatchQueue.main.async {
                        if self.defaultIndex != 0 {
                            self.btnBack.setImage(UIImage(named: "back_black"), for: .normal)
                        } else {
                            self.btnBack.setImage(UIImage(named: "cancel_black"), for: .normal)
                        }
                    }
                }
             
            }
            else {
                
            }
        }
    }
    //MARK: -
    //MARK: -
    
    
    func showAlertItemAddedCartScroll(message: String , isFrontOrBackBool:Bool)
    {
        let alert = UIAlertController(title: "Alert", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
            if isFrontOrBackBool == true {
              self.mainCollectionView.scrollToNextItem()
                self.mainCollectionView.reloadData()
            }
            else {
                self.mainCollectionView.scrollToPreviousItem()
                self.mainCollectionView.reloadData()
            }
           
            
        }))
        self.present(alert, animated: true, completion: nil)
    }
    
    //    MARK:- API CALLING
    func ApiCallToGetSubstituteProduct() {
        let api = "http://gogrocery.ae:81/api/picker-orderlistdetails/" //LIVE
      //  let api = "http://15.185.126.44:8062/api/picker-orderlistdetails/" //DEV
        var params = [String:Any]()
        params["website_id"] = 1
       // params["order_id"] = orderId
        params["order_id"] = self.orderId
        print(params)
        postMethodSubstitute(apiName: api, params: params, vc: self) { (response:JSON) in
            print(response)
            let responseArr = response["response"].arrayValue
            if responseArr.count != 0 {
                let responseDict = responseArr[0]
                print(responseDict)
                let productsTemoArray = responseDict["order_products"].arrayValue
                // self.productsArray = responseDict["order_products"].arrayValue
                
                
                for (_, element) in productsTemoArray.enumerated() {
                    if element["substitute_products"].arrayValue.count != 0 {
                        print(element["substitute_products"].arrayValue.count)
                        self.productsArray.append(element)
                    }
                }
                for _ in self.productsArray {
                    self.submittedPosition.append(false)
                }
                guard self.productsArray.count > 0 else {
                    let alertController = UIAlertController(title: "Alert", message: "You Session has been expired", preferredStyle:.alert)

                    alertController.addAction(UIAlertAction(title: "OK", style: .default)
                    { action -> Void in
                      let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                      let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                        self.navigationController?.pushViewController(vc, animated: true)
                    })
                    self.present(alertController, animated: true, completion: nil)
                    return
                }
                self.lblTitle.text = "Missing item \(self.defaultIndex+1) of \(self.productsArray.count)"
                
                let serverDateDict = self.productsArray[0]["substitute_products"].arrayValue
                let serverDict = serverDateDict[0].dictionaryValue
                let serverDate = serverDict["created_time"]!.stringValue
                print("server recieved date \(serverDate)")
                let convertServerDate = self.utcToLocal(dateStr: serverDate)
                print("utc to local \(String(describing: convertServerDate))")
                let date = Date()
                let df = DateFormatter()
                df.locale = Locale(identifier: "en")
                df.dateFormat = "yyyy-MM-dd HH:mm:ss"
                let deviceDateString = df.string(from: date)
                print("local time \(deviceDateString)")
                let timeDif = self.timeGapBetweenDates(previousDate: convertServerDate!, currentDate: deviceDateString)
                print("total diff sec \(timeDif)")
                
                let substituteTime = responseDict["substitute_approval_time"].intValue
                
                if timeDif <= substituteTime*60 {
                    self.timerCount = (substituteTime*60)-timeDif
                    self.startTimer()
                    self.mainCollectionView.reloadData()
                    
                } else {
                    print("time difference \(timeDif) allowed time \(substituteTime*60)")
                    let alertController = UIAlertController(title: "Alert", message: "Your Session for substitute product has been expired", preferredStyle:.alert)

                    alertController.addAction(UIAlertAction(title: "OK", style: .default)
                    { action -> Void in
                        self.ApiCallToPickerNotification()
                    })
                    self.present(alertController, animated: true, completion: nil)
                }
                
                
                
            }
            else {
                createalert(title: "A!lert", message: response["message"].stringValue, vc: self)
            }

        }
    }
    
    //MARK: - Find deference between two times
    func timeGapBetweenDates(previousDate : String,currentDate : String)-> Int
    {
        let dateString1 = previousDate
        let dateString2 = currentDate

        let Dateformatter = DateFormatter()
        Dateformatter.dateFormat = "yyyy-MM-dd HH:mm:ss"


        let date1 = Dateformatter.date(from: dateString1)
        let date2 = Dateformatter.date(from: dateString2)


        let distanceBetweenDates: TimeInterval? = date2?.timeIntervalSince(date1!)
        let secondsInAnHour: Double = 3600
        let minsInAnHour: Double = 60
        let secondsInDays: Double = 86400
        let secondsInWeek: Double = 604800
        let secondsInMonths : Double = 2592000
        let secondsInYears : Double = 31104000

        let minBetweenDates = Int((distanceBetweenDates! / minsInAnHour))
        let hoursBetweenDates = Int((distanceBetweenDates! / secondsInAnHour))
        let daysBetweenDates = Int((distanceBetweenDates! / secondsInDays))
        let weekBetweenDates = Int((distanceBetweenDates! / secondsInWeek))
        let monthsbetweenDates = Int((distanceBetweenDates! / secondsInMonths))
        let yearbetweenDates = Int((distanceBetweenDates! / secondsInYears))
        let secbetweenDates = Int(distanceBetweenDates!)




        if yearbetweenDates > 0
        {
            print(yearbetweenDates,"years")//0 years
        }
        else if monthsbetweenDates > 0
        {
            print(monthsbetweenDates,"months")//0 months
        }
        else if weekBetweenDates > 0
        {
            print(weekBetweenDates,"weeks")//0 weeks
        }
        else if daysBetweenDates > 0
        {
            print(daysBetweenDates,"days")//5 days
        }
        else if hoursBetweenDates > 0
        {
            print(hoursBetweenDates,"hours")//120 hours
        }
        else if minBetweenDates > 0
        {
            print(minBetweenDates,"minutes")//7200 minutes
        }
        else if secbetweenDates > 0
        {
            print(secbetweenDates,"seconds")//seconds
        }
        return secbetweenDates
    }
    func getDateDiff(start: Date, end: Date) -> Int  {
        let calendar = Calendar.current
        let dateComponents = calendar.dateComponents([Calendar.Component.second], from: start, to: end)

        let seconds = dateComponents.second
        return Int(seconds!)
    }
    
    func ApiCallToSubmitReplacementProduct(isNoSubstitute:Bool = false) {
        
        let mainDict = self.productsArray[defaultIndex].dictionaryValue
        let productDict  = mainDict["product"]?.dictionaryValue
        let productId = productDict!["id"]!.intValue
        
        
        
        let substititArr = mainDict["substitute_products"]!.arrayValue
        
        if isNoSubstitute == true {
            for index in 0 ..< substititArr.count {
                
                let substititDict = substititArr[index].dictionaryValue
                let maxQuantity = substititDict["quantity"]?.intValue
                let subsProductDict  = substititDict["product"]?.dictionaryValue
                let quantity1 = substititDict["quantity"]?.intValue
                let subsProductID = subsProductDict!["id"]!.intValue
                let sProductId = substititDict["substitute_product_id"]!.intValue
                let orderProductId = substititDict["id"]!.intValue
                
                
                var subsPresent = false
                for (_, element) in approvalArray.enumerated() {
                    if "\(subsProductID)" == "\(element["substitute_product_id"] as! Int)"{
                     subsPresent = true
                     break
                    }
                }
                if subsPresent == false {
                   let approvalDict:[String:Any] = ["product_id":productId,"substitute_product_id":subsProductID,"order_product_id":orderProductId,"quantity":quantity1!,"grn_quantity":0]
                    self.approvalArray.append(approvalDict)
                }
                
            }
        }
        
        
        
        //let api = "http://15.185.126.44:8062/api/picker-acceptapproval/" //DEV
        let api = "http://gogrocery.ae:81/api/picker-acceptapproval/" //LIVE
        
         var params = [String:Any]()
         params["website_id"] = 1
         params["user_id"] = UserDefaults.standard.value(forKey: "token") as? String ?? ""
         params["order_id"] = self.orderId
         params["approval_details"] = approvalArray
         print(params)
        let jsonData = try! JSONSerialization.data(withJSONObject: params)
        let jsonString = String(data: jsonData, encoding: .utf8)
        print(jsonString ?? "Wrong data")
         postMethodSubstitute(apiName: api, params: params, vc: self) { (response:JSON) in
             print(response)
             let responseArr = response["response"].arrayValue
            
            if response["status"].intValue != 0 {
                
                self.AfterSubmitResponse(message: response["message"].stringValue,noSubstitute: isNoSubstitute)
             }
             else {
                let alertController = UIAlertController(title: "Alert", message: response["message"].stringValue, preferredStyle:.alert)

                alertController.addAction(UIAlertAction(title: "OK", style: .default)
                { action -> Void in
                  let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                  let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                  self.navigationController?.pushViewController(vc, animated: true)
                })
                self.present(alertController, animated: true, completion: nil)
                 
             }

         }
    }
    
    func ApiCallToResetOrder() {
       // let api = "http://15.185.126.44:8062/api/picker-resetsendapproval/"
         let api = "http://gogrocery.ae:81/api/picker-resetsendapproval/" //LIVE
         var params = [String:Any]()
         params["website_id"] = 1
         params["order_id"] = self.orderId
         print(params)
         postMethodSubstitute(apiName: api, params: params, vc: self) { (response:JSON) in
             print(response)
            if response["status"].intValue != 0 {
                self.ApiCallToPickerNotification()
             }
             else {
                self.ApiCallToPickerNotification()
             }

         }
    }
    
    func ApiCallToPickerNotification(isSuccess:Bool = false) {
        
      //  let api = "http://15.185.126.44:8062/api/picker-sendpushnotification/"
        let api = "http://gogrocery.ae:81/api/picker-sendpushnotification/"
         var params = [String:Any]()
         params["order_id"] = self.orderId
         print(params)
         postMethodSubstitute(apiName: api, params: params, vc: self) { (response:JSON) in
             print(response)
            if isSuccess == false {
                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
                self.navigationController?.pushViewController(vc, animated: true)
            } else {
                let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "SusbtituteSucccessViewController") as! SusbtituteSucccessViewController
                self.navigationController?.pushViewController(vc, animated: true)
            }
            
         }
    }
    
    func AfterSubmitResponse(message:String = "",noSubstitute:Bool = false) {
        print(approvalArray.count)
        self.submittedPosition[defaultIndex] = true
        let mainDict = self.productsArray[defaultIndex].dictionaryValue
        let mainproductId = mainDict["id"]!.intValue
        self.substituteSubmitted.append(mainproductId)
        print("approved")
        print(approvalArray)
        maxQuantityCheck = 0
        approvalArray.removeAll()
        if noSubstitute == true {
            let productDict  = mainDict["product"]?.dictionaryValue
            let productId = productDict!["id"]!.intValue
            var indexArray = [Int]()
            for (index, element) in localCartArray.enumerated() {
                if "\(productId)" == "\(element["main_product_id"] as! String)"{
                    indexArray.append(index)
                     
                }
            }
            self.localCartArray.remove(at: indexArray)
            
        }
        var goTo = 0
        var forward = false
        for index in defaultIndex ..< self.productsArray.count {
            if self.submittedPosition[index] == false {
                goTo = index
                forward = true
                break
            }
        }
        if forward == false {
            for i in stride(from: defaultIndex, through: 0, by: -1) {
                if self.submittedPosition[i] == false {
                    goTo = i
                    forward = true
                    break
                }
            }
        }
        var msg = ""
        if noSubstitute == false {
            msg = "You have successfully added substitute products"
        } else {
            msg = message
        }
        if forward == true {
            
            let alertController = UIAlertController(title: "Success", message: msg, preferredStyle:UIAlertController.Style.alert)

            alertController.addAction(UIAlertAction(title: "OK", style: .default)
            { action -> Void in
              if goTo > self.defaultIndex {
                  let previousIndex = self.defaultIndex
                  self.lblTitle.text = "Missing item \(goTo+1) of \(self.productsArray.count)"
                  self.defaultIndex = goTo
                  goTo = goTo - previousIndex
                  self.mainCollectionView.reloadData()
                  self.mainCollectionView.scrollToNextItem(position: CGFloat(goTo))
                  DispatchQueue.main.async {
                    if self.defaultIndex != 0 {
                          self.btnBack.setImage(UIImage(named: "back_black"), for: .normal)
                      } else {
                          self.btnBack.setImage(UIImage(named: "cancel_black"), for: .normal)
                      }
                  }
                  
              } else {
                  let previousIndex = self.defaultIndex
                  self.lblTitle.text = "Missing item \(goTo+1) of \(self.productsArray.count)"
                  self.defaultIndex = goTo
                  goTo = previousIndex - goTo
                  self.mainCollectionView.reloadData()
                  self.mainCollectionView.scrollToPreviousItem(position: CGFloat(goTo))
                  self.mainCollectionView.reloadData()
                  DispatchQueue.main.async {
                    if self.defaultIndex != 0 {
                          self.btnBack.setImage(UIImage(named: "back_black"), for: .normal)
                      } else {
                          self.btnBack.setImage(UIImage(named: "cancel_black"), for: .normal)
                      }
                  }
              }
            })
            self.present(alertController, animated: true, completion: nil)

            
            
        } else {
            
            let alertController = UIAlertController(title: "Success", message: msg, preferredStyle:.alert)

            alertController.addAction(UIAlertAction(title: "OK", style: .default)
            { action -> Void in
                self.ApiCallToPickerNotification()
            })
            self.present(alertController, animated: true, completion: nil)

            
                
            
        }
         //mainCollectionView.scrollToNextItem()
        
    }
    
}
//MARK: - CollectionView Datasourse and delegets
//MARK: -
extension SubstituteViewController : UICollectionViewDataSource, UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        if collectionView.tag == 0 {
            return self.productsArray.count
        }
        else if collectionView.tag == 1 {
             //return 4
            return self.productsArray[defaultIndex]["substitute_products"].arrayValue.count
        }
        else {
            return 0
        }
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        if collectionView.tag == 0 {
            //print("parent index \(indexPath.row)")
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "MainCollectionViewCell", for: indexPath) as! MainCollectionViewCell
            cell.layoutIfNeeded()
            let mainDict = self.productsArray[indexPath.row].dictionaryValue
            let productDict  = mainDict["product"]?.dictionaryValue
            let mainproductId = mainDict["id"]!.intValue
            let maxQuantity = mainDict["shortage"]?.intValue
            
            print("submitted \(substituteSubmitted)")
            if self.substituteSubmitted.contains(mainproductId) {
                cell.submittedView.alpha = 1
                
            } else {
                cell.submittedView.alpha = 0
            }
            cell.lblOutOfStock.text = "Out Of Stock"
            cell.lblOutOfStock.textColor = UIColor(named: "buttonColor")
            cell.lblProductName.text = productDict!["name"]?.stringValue
            
            
            cell.lblChooseAReplacement.text = "Choose Replacemet : Max  \(maxQuantity ?? 0) Quantity"
            let uomDict = productDict!["uom"]!.dictionaryValue
            let quantityType = uomDict["uom_full_name"]!.stringValue
            let weight = productDict!["weight"]!.stringValue
            cell.lblProductWeight.text = "\(weight) \(quantityType)"
            
            let pp = mainDict["product_price"]?.doubleValue ?? 0
            let ppp = String(format: "%.2f", pp)
            cell.lblProductPrice.text = "AED \(ppp)"
            let productImageArr = productDict!["product_images"]!.arrayValue
            let productImageDict = productImageArr[0]
            let imageLinkUrl = productImageDict["link"].stringValue
            if  (productImageDict["img"].string)!.isEmpty == false {
                let imgUrl = productImageDict["img"].stringValue
                let fullUrl = imageLinkUrl + imgUrl
                let url = URL(string: fullUrl)
                cell.imgMain.sd_setImage(with: url!)
            }
            else {
                cell.imgMain.image = UIImage(named:"no_image")
            }
            
            return cell
        }
        else {
            let cell1 = collectionView.dequeueReusableCell(withReuseIdentifier: "SubstituteCollectionViewCell", for: indexPath) as! SubstituteCollectionViewCell
           
            cell1.btnAddtoCart.tag = indexPath.row
            cell1.btnAddtoCart.addTarget(self, action: #selector(addToCartbtnAction), for: .touchUpInside)
            cell1.btnPlus.tag = indexPath.row
            cell1.btnPlus.addTarget(self, action: #selector(btnPlusAction), for: .touchUpInside)
            cell1.btnMinus.tag = indexPath.row
            cell1.btnMinus.addTarget(self, action: #selector(btnMinusAction), for: .touchUpInside)
            
            
            let substititArr = self.productsArray[defaultIndex]["substitute_products"].arrayValue
            let substititDict = substititArr[indexPath.row].dictionaryValue
            let subsProductDict  = substititDict["product"]?.dictionaryValue
            cell1.lblSubProductName.text = subsProductDict!["name"]?.stringValue
            cell1.lblSKUName.text = "SKU : \(subsProductDict!["sku"]!.stringValue)"
            //print("mainindex \(mainCollectionIndex) subIndex \(indexPath.row)")
            //print("Product Name ------------>>>>>> \(String(describing: cell1.lblSubProductName.text))")
            
            let uomDict = subsProductDict!["uom"]!.dictionaryValue
            let quantityType = uomDict["uom_full_name"]!.stringValue
            let weight = subsProductDict!["weight"]!.stringValue
            cell1.lblSubProductWeight.text = "\(weight) \(quantityType)"
            
            let pp = substititDict["product_price"]?.doubleValue ?? 0
            let ppp = String(format: "%.2f", pp)
            cell1.lblSubProductPrice.text = "AED \(ppp)"
            
            let productImageArr = subsProductDict!["product_images"]!.arrayValue
            let productImageDict = productImageArr[0]
            let imageLinkUrl = productImageDict["link"].stringValue
            if  (productImageDict["img"].string)!.isEmpty == false {
                let imgUrl = productImageDict["img"].stringValue
                let fullUrl = imageLinkUrl + imgUrl
                let url = URL(string: fullUrl)
                cell1.imgSubsImg.sd_setImage(with: url!)
            }
            else {
                cell1.imgSubsImg.image = UIImage(named:"no_image")
            }
            let productId = subsProductDict!["id"]!.intValue
            /*
            for index in cartDatafromDb {
                if "\(productId)" == index.product_id {
                    if let quant = index.quantity {
                        let inttype: Int = Int(quant) ?? 0
                        DispatchQueue.main.async {
                            cell1.btnAddtoCart.setTitle("\(inttype)", for: .normal)
                            cell1.btnPlus.isHidden = false
                            cell1.btnMinus.isHidden = false
                            cell1.btnAddtoCart.backgroundColor = .white
                            cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                            cell1.cartStack.layer.cornerRadius = 5
                            cell1.cartStack.clipsToBounds = true
                            cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                            cell1.cartStack.layer.borderWidth = 1
                        }
                    }
                }
                else {
                    cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                    cell1.btnPlus.isHidden = true
                    cell1.btnMinus.isHidden = true
                    cell1.btnAddtoCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
                    cell1.btnAddtoCart.setTitleColor(.white, for: .normal)
                    cell1.cartStack.layer.cornerRadius = 5
                    cell1.cartStack.clipsToBounds = true
                    cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1.cartStack.layer.borderWidth = 1


                }
            */
            print(localCartArray)
            if localCartArray.count == 0 {
                cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                cell1.btnPlus.isHidden = true
                cell1.btnMinus.isHidden = true
                cell1.btnAddtoCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
                cell1.btnAddtoCart.setTitleColor(.white, for: .normal)
                cell1.cartStack.layer.cornerRadius = 5
                cell1.cartStack.clipsToBounds = true
                cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                cell1.cartStack.layer.borderWidth = 1
            }
            
            for index in localCartArray {
                if "\(productId)" == index["product_id"] as! String {
                    let quantt = index["quantity"] as! String
                    cell1.btnAddtoCart.setTitle("\(quantt)", for: .normal)
                        cell1.btnPlus.isHidden = false
                        cell1.btnMinus.isHidden = false
                        cell1.btnAddtoCart.backgroundColor = .white
                        cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                        cell1.cartStack.layer.cornerRadius = 5
                        cell1.cartStack.clipsToBounds = true
                        cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                        cell1.cartStack.layer.borderWidth = 1
                    break
                }
                else {
                    cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                    cell1.btnPlus.isHidden = true
                    cell1.btnMinus.isHidden = true
                    cell1.btnAddtoCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
                    cell1.btnAddtoCart.setTitleColor(.white, for: .normal)
                    cell1.cartStack.layer.cornerRadius = 5
                    cell1.cartStack.clipsToBounds = true
                    cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                    cell1.cartStack.layer.borderWidth = 1
                }
            }
            
             cell1.layoutIfNeeded()
            return cell1
        }
    }
    func collectionView(_ collectionView: UICollectionView, willDisplay cell: UICollectionViewCell, forItemAt indexPath: IndexPath) {
        
        if collectionView == mainCollectionView {
            guard let cell = cell as? MainCollectionViewCell else { return }
            cell.subsCollectionView.dataSource = self
            cell.subsCollectionView.delegate = self
            cell.layoutIfNeeded()
            self.mainCollectionIndex = indexPath.row
            print("Index Path --------------------------->>>>>>>\(indexPath.row)")
            cell.subsCollectionView.reloadData()
            
            
            //  self.view.layoutIfNeeded()
        }
    }
    
    
    
    
}


//MARK: - CollectionView DelegetsFlowLayout
//MARK: -
extension SubstituteViewController : UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        if collectionView.tag == 0 {
            return CGSize(width: mainCollectionView.frame.width, height: mainCollectionView.frame.height)
        }
        else if collectionView.tag == 1 {
            
            let numberOfItemsPerRow:CGFloat = 3.0
            let spacingBetweenCells:CGFloat = 0
            let totalSpacing = (2 * self.spacing) + ((numberOfItemsPerRow - 1) * spacingBetweenCells) //Amount of total spacing in a row
            //if let collection = self.mainCollectionView {
            let swidth = (UIScreen.main.bounds.width-12)/3
            //   let width = (self.mainCollectionView.bounds.width)/numberOfItemsPerRow
            return CGSize(width: swidth, height: 270)
            
            //   }
            //  else{
            //      return CGSize(width: 0, height: 0)
            // }
            
            //  return CGSize(width: 200, height: 300)
        }
        else  {
            return CGSize(width: 0, height: 0)
        }
    }
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 1
    }
    
}
extension UICollectionView {
    func scrollToNextItem(position:CGFloat = 1) {
        let contentOffset = CGFloat(floor(self.contentOffset.x + (self.bounds.size.width*position)))
        self.moveToFrame(contentOffset: contentOffset)
    }
    
    func scrollToPreviousItem(position:CGFloat = 1) {
        let contentOffset = CGFloat(floor(self.contentOffset.x - (self.bounds.size.width*position)))
        self.moveToFrame(contentOffset: contentOffset)
    }
    
    func moveToFrame(contentOffset : CGFloat) {
        self.setContentOffset(CGPoint(x: contentOffset, y: self.contentOffset.y), animated: true)
    }
}
extension Array {
  mutating func remove(at indexes: [Int]) {
    for index in indexes.sorted(by: >) {
      remove(at: index)
    }
  }
}
