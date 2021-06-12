//
//  OrderPlacedViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 01/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
import FirebaseAnalytics
class OrderPlacedViewController: UIViewController {
    @IBOutlet weak var viewContinueShopping: UIView!
    @IBOutlet weak var viewOrderPlaced: UIView!
    @IBOutlet weak var viewTotalAmount: UIView!
    @IBOutlet weak var viewAmountCalculation: UIView!
    @IBOutlet weak var viewAddress: UIView!
    @IBOutlet weak var lblOrderId: UILabel!
    @IBOutlet weak var lblSubTotal: UILabel!
    @IBOutlet weak var lblDiscount: UILabel!
    @IBOutlet weak var lblDeliveryCharge: UILabel!
    @IBOutlet weak var lblTotalAmount: UILabel!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var lblApartment: UILabel!
    @IBOutlet weak var lblCountry: UILabel!
    @IBOutlet weak var lblMobile: UILabel!
    @IBOutlet weak var btnContinueShopping: UIButton!
    @IBOutlet weak var viewOrderPlacedHeight: NSLayoutConstraint!
    @IBOutlet weak var imgImage: UIImageView!
    @IBOutlet weak var lblTitle: UILabel!
    @IBOutlet weak var lblSubTitle: UILabel!
    @IBOutlet weak var lblPara: UILabel!
    @IBOutlet weak var lblTitleHeight: NSLayoutConstraint!
    @IBOutlet weak var lblSubTitleHeight: NSLayoutConstraint!
    @IBOutlet weak var lblParaHeight: NSLayoutConstraint!
    var orderId = String()
    var orderIdString:String?
    var subTotal = String()
    var discount = String()
    var deliveryCharge = String()
    var total = String()
    var addrDict = [String:JSON]()
    var orderStatus = String()
    var orderType = String()
    var paymentStatus = String()
    var succFailRes = NSMutableDictionary()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        

//        btnContinueShopping.addShadow2()

        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        viewOrderPlaced.addShadow2()
        viewAmountCalculation.addShadow2()
        viewAddress.addShadow2()
        viewContinueShopping.addShadow2()
        lblOrderId.layer.cornerRadius = lblOrderId.frame.height/2
        lblOrderId.layer.masksToBounds = true
        DiplayDefaultAddress()
        self.navigationController?.isNavigationBarHidden = true
    }
    
    func  DiplayDefaultAddress() {
        if self.orderType == "Credit / Debit Card(Online Payment)" {
            print(succFailRes)
            if orderStatus == "Success" {
                paymentStatus = "Success"
                self.imgImage.image = UIImage(named: "success_image")
                self.lblTitle.text = "Order successful. "
                self.lblTitle.textColor = UIColor(named: "buttonBackgroundColor")
                self.lblTitleHeight.constant = 25.0
                self.lblSubTitleHeight.constant = 25
                self.lblSubTitle.textColor = UIColor(named: "buttonBackgroundColor")
                self.lblParaHeight.constant = 45
                self.lblSubTitle.isHidden = false
                self.lblPara.isHidden = false
                self.viewOrderPlacedHeight.constant = 210
                self.lblName.text = addrDict["delivery_name"]!.stringValue
                self.lblApartment.text = addrDict["delivery_street_address"]!.stringValue
                self.lblCountry.text = addrDict["delivery_state_name"]!.stringValue + " " + addrDict["delivery_country_name"]!.stringValue
                self.lblMobile.text = addrDict["delivery_phone"]!.stringValue
                self.lblOrderId.text = "Your Order ID : \(orderId)"
                self.lblSubTotal.text = subTotal
                self.lblDiscount.text = discount
                self.lblDeliveryCharge.text = deliveryCharge
                self.lblTotalAmount.text = total
                self.btnContinueShopping.layer.cornerRadius = 5
                self.btnContinueShopping.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                self.btnContinueShopping.layer.borderWidth = 1
                self.btnContinueShopping.setTitle("CONTINUE SHOPPING", for: .normal)
                self.btnContinueShopping.setTitleColor(UIColor(named: "buttonBackgroundColor"), for: .normal)
               // PurchaseEvent(order_id : "\(orderId)")
//                let dictParam :[String:Any] = ["Content_ID":"\(orderId)","Currency": "AED", "ValueToSum":"\(self.lblTotalAmount.text!)"]
//                print(dictParam)
//                self.PurchaseEvents(dictParam: dictParam)
                UserDefaults.standard.setValue("", forKey: "addNote")
                UserDefaults.standard.synchronize()
                
                let checkOutItemNamesWithQauntity = ["orderId": "sample#001", "OrderFrom":"Android","customer_name": "Pankaj Pandit","paymentMethod": "Credit Card","TransactionId" : "41452174574574", "payment_status": "success"]

                let dictParam :[String:Any] = ["contents":checkOutItemNamesWithQauntity,"Currency": "AED", "ValueToSum":"\(self.lblTotalAmount.text!)"]
                //logParms.contents = checkOutItemNamesWithQauntity //
             //   logParms.value = response['data']['orderamountdetails']['grand_total']; // orde total
             //   logParms.currency = 'AED'; // currency
                //this._globalService.facebookPixelEventLog('track','AddPaymentInfo',logParms);
                
                

            }
            else   {
                paymentStatus = "Failed"
                self.imgImage.image = UIImage(named: "remove")
                self.lblTitle.text = "Your payment has been failed"
                self.lblTitle.textColor = UIColor(named: "buttonColor")
                self.lblTitleHeight.constant = 25.0
                self.lblSubTitleHeight.constant = 0
                self.lblParaHeight.constant = 0
                self.lblSubTitle.isHidden = true
                self.lblPara.isHidden = true
                self.viewOrderPlacedHeight.constant = 150
                self.lblName.text = addrDict["delivery_name"]!.stringValue
                self.lblApartment.text = addrDict["delivery_street_address"]!.stringValue
                self.lblCountry.text = addrDict["delivery_state_name"]!.stringValue + " " + addrDict["delivery_country_name"]!.stringValue
                self.lblMobile.text = addrDict["delivery_phone"]!.stringValue
                self.lblOrderId.text = "Your Order ID : \(orderId)"
                self.lblSubTotal.text = subTotal
                self.lblDiscount.text = discount
                self.lblDeliveryCharge.text = deliveryCharge
                self.lblTotalAmount.text = total
//                self.btnContinueShopping.setTitleColor(.clear, for: .normal)
//                self.btnContinueShopping.setTitleColor(.red, for: .normal)
                self.btnContinueShopping.setTitle("Retry Payment", for: .normal)
                self.btnContinueShopping.setTitleColor(UIColor(named: "buttonColor"), for: .normal)
                self.btnContinueShopping.layer.cornerRadius = 5
                self.btnContinueShopping.layer.borderColor = UIColor(named: "buttonColor")?.cgColor
                self.btnContinueShopping.layer.borderWidth = 1
                let dictParam :[String:Any] = ["Content_ID":"\(orderId)","Currency": "AED", "ValueToSum":"\(self.lblTotalAmount.text!)"]
                print(dictParam)
                self.PurchaseFailedEvent(dictParam: dictParam)
             //   self.PurchaseFailedEvent(order_id : "\(orderId)")
            }
        }
        else {
            if orderStatus == "Success" {
                paymentStatus = "Success"
               // self.imgImage.image = UIImage(named: "success_image")
                self.imgImage.image = UIImage(named: "success_image")
                self.lblTitle.text = "Order successful. "
                self.lblTitle.textColor = UIColor(named: "buttonBackgroundColor")
                self.lblTitleHeight.constant = 25.0
                self.lblSubTitleHeight.constant = 25
                self.lblSubTitle.textColor = UIColor(named: "buttonBackgroundColor")
                self.lblParaHeight.constant = 45
                self.lblSubTitle.isHidden = false
                self.lblPara.isHidden = false
                self.viewOrderPlacedHeight.constant = 210
                self.lblName.text = addrDict["delivery_name"]!.stringValue
                self.lblApartment.text = addrDict["delivery_street_address"]!.stringValue
                self.lblCountry.text = addrDict["delivery_state_name"]!.stringValue + " " + addrDict["delivery_country_name"]!.stringValue
                self.lblMobile.text = addrDict["delivery_phone"]!.stringValue
                self.lblOrderId.text = "Your Order ID : \(orderId)"
                self.lblSubTotal.text = subTotal
                self.lblDiscount.text = discount
                self.lblDeliveryCharge.text = deliveryCharge
                self.lblTotalAmount.text = total
                self.btnContinueShopping.layer.cornerRadius = 5
                self.btnContinueShopping.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                self.btnContinueShopping.layer.borderWidth = 1
                self.btnContinueShopping.setTitle("CONTINUE SHOPPING", for: .normal)
                self.btnContinueShopping.setTitleColor(UIColor(named: "buttonBackgroundColor"), for: .normal)
                let dictParam :[String:Any] = ["Content_ID":"\(orderId)","Currency": "AED", "ValueToSum":"\(self.lblTotalAmount.text!)"]
                print(dictParam)
                self.PurchaseEvents(dictParam: dictParam)
                UserDefaults.standard.setValue("", forKey: "addNote")
                UserDefaults.standard.synchronize()
            }
            else {
                paymentStatus = "Failed"
                self.imgImage.image = UIImage(named: "remove")
                self.lblTitle.text = "Your payment has been failed"
                self.lblTitle.textColor = UIColor(named: "buttonColor")
                self.lblTitleHeight.constant = 25.0
                self.lblSubTitleHeight.constant = 0
                self.lblParaHeight.constant = 0
                self.lblSubTitle.isHidden = true
                self.lblPara.isHidden = true
                 self.viewOrderPlacedHeight.constant = 150
                self.lblName.text = addrDict["delivery_name"]!.stringValue
                self.lblApartment.text = addrDict["delivery_street_address"]!.stringValue
                self.lblCountry.text = addrDict["delivery_state_name"]!.stringValue + " " + addrDict["delivery_country_name"]!.stringValue
                self.lblMobile.text = addrDict["delivery_phone"]!.stringValue
                self.lblOrderId.text = "Your Order ID : \(orderId)"
                self.lblSubTotal.text = subTotal
                self.lblDiscount.text = discount
                self.lblDeliveryCharge.text = deliveryCharge
                self.lblTotalAmount.text = total
                self.btnContinueShopping.setTitle("Retry Payment", for: .normal)
                self.btnContinueShopping.setTitleColor(UIColor(named: "buttonColor"), for: .normal)
                self.btnContinueShopping.layer.cornerRadius = 5
                self.btnContinueShopping.layer.borderColor = UIColor(named: "buttonColor")?.cgColor
                self.btnContinueShopping.layer.borderWidth = 1
                let dictParam :[String:Any] = ["Content_ID":"\(orderId)","Currency": "AED", "ValueToSum":"\(self.lblTotalAmount.text!)"]
                print(dictParam)
            }
        }
    }
    
    @IBAction func btnContinueShoppingAction(_ sender: Any) {
        if paymentStatus == "Failed" {
            if let viewControllers = self.navigationController?.viewControllers
            {
                for aViewController in viewControllers {
                    if aViewController is DeliveryDetailsViewController {
                        let delObj = DeliveryDetailsViewController()
                        delObj.paymentStatusFromPlaced = paymentStatus
                        delObj.orderIdFromPlaced = orderId
                        self.navigationController?.popToViewController(aViewController, animated: true)
                    }
                }
            }
        }
        else {
            self.ApiCallToEmptyCart()
        }
    }
    
    func ApiCallToEmptyCart() {
        if UserDefaults.standard.value(forKey: "is-login") != nil {
            let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
            let para:[String:Any] = ["website_id":"1" , "device_id":deviceID]
            postMethodReturnWithAuthorizationJson(apiName: "empty-cart/", params: para, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
               let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
               let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
               self.navigationController?.pushViewController(vc, animated: true)
                }
            }
        }
    }
    
//   MARK:-  Events
       func PurchaseEvents(dictParam : [String:Any]) {
        Analytics.logEvent("purchase_events", parameters: dictParam)
    }
    func PurchaseFailedEvent(dictParam : [String:Any]) {
         Analytics.logEvent("PurchaseFailed", parameters: dictParam)
     }
}
