
//
//  NewPaymentViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 16/04/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
 import CCAvenueSDK
import SwiftyJSON
import FirebaseAnalytics
class CCPaymentViewController: UIViewController ,CCAvenuePaymentControllerDelegate {
  //  var paymentController = CCAvenuePaymentController()
    
    //    MARK:- Outlet Declaration
    @IBOutlet weak var viewDeliveryAddress: UIView!
    @IBOutlet weak var viewDeliveryData: UIView!
    @IBOutlet weak var viewOrderSummary: UIView!
    @IBOutlet weak var viewAmount: UIView!
    @IBOutlet weak var viewTotalAmpont: UIView!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var lblApartment: UILabel!
    @IBOutlet weak var lblCountry: UILabel!
    @IBOutlet weak var lblMobile: UILabel!
    @IBOutlet weak var btnChangeOrAddAddress: UIButton!
    @IBOutlet weak var lblSubTotal1: UILabel!
    @IBOutlet weak var lblDefault: UILabel!
    @IBOutlet weak var lblDiscount: UILabel!
    @IBOutlet weak var lblDeliveryCharges: UILabel!
    @IBOutlet weak var lblTotalAmount: UILabel!
    @IBOutlet weak var lblTotalLast: UILabel!
    @IBOutlet weak var btnContinue: UIButton!
    @IBOutlet weak var viewContinue: UIView!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var viewPaymentHeight: NSLayoutConstraint!
    
    var paymentMode:String = ""
    var addressSelect = String()
    var paymentInfoDict = [String:JSON]()
    var addressId = Int()
    var defaultAddressDict1 = [String:JSON]()
    var paymentMethodArr = [JSON]()
    var orderId = String()
    //    var orderId = UserDefaults.standard.value(forKey: "order_id") as! String
    var customerOrderId = String()
    var paymentId = Int()
    var paymentgateway_type_id = Int()
    var showAdd = "N"
    var useCCPromo = "N"
    var validateAdd = "N"
    
    
    var merchantIDTF = String()
    var acessCodeTF = String()
    var currencyTF = String()
    var amountTF = String()
    var custIDTF = String()
    var orderIDTF = String()
    var billingNameTF = String()
    var billingAddressTF = String()
    var billingCityTF = String()
    var billingStateTF = String()
    var billingCountryTF = String()
    var billingTelTF = String()
    var billingEmailTF = String()
    var shippingNameTF = String()
    var shippingAddressTF = String()
    var shippingCityTF = String()
    var shippingStateTF = String()
    var shippingCountry = String()
    var shippingTelTF = String()
    var rsaKeyURLTF = String()
    var redirectURLTF = String()
    var cancelURLTF = String()
    var showAddSwitch = String()
    var useCCPromoSwitch = String()
    var merchant_param1 = String()
    var merchant_param2 = String()
    var orderIDInPayment = Int()
    var paymentTokenInReset: String = ""
    var pageFrom:String = ""
    var paymentIdArr = [Int]()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        self.paymentIdArr.removeAll()
        viewContinue.addShadow1()
        viewDeliveryData.addShadow2()
        viewAmount.addShadow2()
        viewTotalAmpont.addShadow2()
        viewContinue.addShadow2()
        btnChangeOrAddAddress.layer.cornerRadius = 5
        //  btnChangeOrAddAddress.addShadow2()
        self.lblDefault.layer.cornerRadius = self.lblDefault.frame.height/2
        self.lblDefault?.layer.masksToBounds = true
        self.btnContinue.layer.cornerRadius = 5
        self.btnContinue.addShadow2()
        ApiCallToGetPaymentMethod()
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = false
        if let orderIdd = UserDefaults.standard.value(forKey: "order_id") as? String {
            orderId = orderIdd
            print(orderId)
        }
        if let customerOrderIdd = UserDefaults.standard.value(forKey: "custom_order_id") as? String {
            customerOrderId = customerOrderIdd
            print(customerOrderId)
        }
        self.navigationController?.isNavigationBarHidden = false
       // allUnselect()
        ApiCallToGetOrderInfo()
        ApiCallTogetUserDetails()
    }
    
    // MARK: - Button Actions
    // MARK: -

    @IBAction func btnAddOrChangeAddressAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "SavedAdressListViewController") as! SavedAdressListViewController
        vc.pageTypeFromCheckOut = "Payment"
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnContinueAction(_ sender: Any) {
      //  MakePayment()
        if paymentMode.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please select Payment Method", vc: self)
        }
//        if paymentIdArr.count == 0 {
//           createalert(title: "Alert", message: "Please select Payment Method", vc: self)
//        }
        else if paymentMode == "Credit / Debit Card(Online Payment)" {
           // ApicallToGetTransactionID()
            //self.MakePayment()
            self.MakeDemoPayment()
        }
        else {
            self.ApiCallToBookProduct()
        }
    }

//    func cashOnDeliverySelect() {
//          self.imgRadioCash.image = UIImage(named: "radio_select")
//          paymentMode = "Cash On Delivery"
//          self.paymentId = 16
//          self.paymentgateway_type_id = 4
//
//      }
//      func cardSelect() {
//          self.imgRadioCard.image = UIImage(named: "radio_select")
//          paymentMode = "Credit / Debit Card"
//          self.paymentId = 51
//          self.paymentgateway_type_id = 2
//        ApicallToGetTransactionID()
//      }
//      func cardOnDeliverySelect() {
//          self.imgRadioCardOnDelivery.image = UIImage(named: "radio_select")
//          paymentMode = "Card On Delivery"
//          self.paymentId = 59
//          self.paymentgateway_type_id = 4
//      }
//
//      func allUnselect() {
//          self.imgRadioCash.image = UIImage(named: "radio_unselect")
//          self.imgRadioCard.image = UIImage(named: "radio_unselect")
//          self.imgRadioCardOnDelivery.image = UIImage(named: "radio_unselect")
//          paymentMode = ""
//      }
    
    func getAddressFromApiCall(){
        self.lblName.text = paymentInfoDict["delivery_name"]?.string ?? ""
        //self.lblName.text = paymentInfoDict["delivery_name"]!.stringValue
        //  print(self.lblApartment.text)
        self.lblApartment.text = paymentInfoDict["delivery_street_address"]?.string ?? ""
        self.lblCountry.text = paymentInfoDict["delivery_state_name"]!.stringValue + " " + paymentInfoDict["delivery_country_name"]!.stringValue
        self.lblMobile.text = paymentInfoDict["delivery_phone"]?.string ?? ""
        self.addressId = paymentInfoDict["id"]?.int ?? 0
        
     //   username
       // self.billingNameTF = UserDefaults.standard.value(forKey: "username") as String
        self.billingNameTF = paymentInfoDict["delivery_name"]?.string ?? ""
        self.billingAddressTF = paymentInfoDict["delivery_street_address"]?.string ?? ""
        self.billingCityTF = paymentInfoDict["delivery_country_name"]?.string ?? ""
        self.billingStateTF = paymentInfoDict["delivery_country_name"]?.string ?? ""
        self.billingCountryTF = paymentInfoDict["delivery_country_name"]?.string ?? ""
        self.billingTelTF = paymentInfoDict["delivery_phone"]?.string ?? ""
        
        self.shippingNameTF = paymentInfoDict["delivery_name"]?.string ?? ""
        self.shippingAddressTF = paymentInfoDict["delivery_street_address"]?.string ?? ""
        self.shippingCityTF = paymentInfoDict["delivery_country_name"]?.string ?? ""
        self.shippingStateTF = paymentInfoDict["delivery_country_name"]?.string ?? ""
        self.shippingCountry = paymentInfoDict["delivery_country_name"]?.string ?? ""
        self.shippingTelTF = paymentInfoDict["delivery_phone"]?.string ?? ""
        
    }
    func getAddressFromList(){
        
         self.lblName.text = defaultAddressDict1["delivery_name"]?.string ?? ""
     //   self.lblName.text = defaultAddressDict1["delivery_name"]!.stringValue
        self.lblApartment.text = defaultAddressDict1["delivery_street_address"]?.string ?? ""
        self.lblCountry.text = defaultAddressDict1["delivery_state_name"]!.stringValue + " " + defaultAddressDict1["delivery_country_name"]!.stringValue
        self.lblMobile.text = defaultAddressDict1["delivery_phone"]?.string ?? ""
        self.addressId = defaultAddressDict1["id"]?.int ?? 0
        
        self.billingNameTF = defaultAddressDict1["delivery_name"]?.string ?? ""
       // self.billingNameTF = defaultAddressDict1["delivery_name"]!.stringValue
        self.billingAddressTF = defaultAddressDict1["delivery_street_address"]?.string ?? ""
        self.billingCityTF = defaultAddressDict1["delivery_state_name"]?.string ?? ""
        self.billingStateTF = defaultAddressDict1["delivery_state_name"]?.string ?? ""
        self.billingCountryTF = defaultAddressDict1["delivery_country_name"]?.string ?? ""
        self.billingTelTF = defaultAddressDict1["delivery_phone"]?.string ?? ""
        
        self.shippingNameTF =  defaultAddressDict1["delivery_name"]?.string ?? ""
        self.shippingAddressTF = defaultAddressDict1["delivery_street_address"]?.string ?? ""
        self.shippingCityTF = defaultAddressDict1["delivery_state_name"]?.string ?? ""
        self.shippingStateTF = defaultAddressDict1["delivery_state_name"]?.string ?? ""
        self.shippingCountry = defaultAddressDict1["delivery_country_name"]?.string ?? ""
        self.shippingTelTF = defaultAddressDict1["delivery_phone"]?.string ?? ""
    }
    func getAmountDetails() {
        print(paymentInfoDict)
        //subTotal
        self.lblSubTotal1.text = "AED \(String(describing: paymentInfoDict["net_amount"]?.double ?? 0.00))"
        self.lblDiscount.text = "AED \(String(describing: paymentInfoDict["cart_discount"]?.double ?? 0.00))"
        self.lblDeliveryCharges.text = "AED \(String(describing: paymentInfoDict["shipping_cost"]?.double ?? 0.00))"
        self.lblTotalAmount.text = "AED \(String(describing: paymentInfoDict["gross_amount_base"]?.double ?? 0.00))"
        self.lblTotalLast.text = "AED \(String(describing: paymentInfoDict["gross_amount"]?.double ?? 0.00))"
        self.amountTF = "\(paymentInfoDict["gross_amount"]?.int ?? 0)"
    }
    //    MARK:- Api Calling
    func ApiCallToGetOrderInfo() {
        let auth = UserDefaults.standard.value(forKey: "token") as? String ?? ""
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as? Int ?? 0
        let headers:[String : Any] = ["Authorization": "Token \(auth)","WAREHOUSE":"\(wareHouseId)","WID":"1" , "Content-Type": "application/json"]
            print(self.orderId)
            getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "order-details/\(self.orderId)/", vc: self, header: headers) { (response) in
                print(response)
                if response["status"].stringValue == "200" {
                    self.paymentInfoDict = response["data"].dictionaryValue
                    self.orderIDInPayment =  self.paymentInfoDict["id"]?.int ?? 0
                     print( self.customerOrderId)
                    print( self.orderIDInPayment)
                    // self.getAddressFromApiCall()
                    if self.addressSelect == "yes" {
                        self.getAddressFromList()
                        self.getAmountDetails()
                    }
                    else {
                        self.getAddressFromApiCall()
                        self.getAmountDetails()
                    }
                }
                else {
                    self.showAlertOnOrderInfo(message: "You are not authorise to view this order.")
                }
            }
    }
    func ApiCallTogetUserDetails() {
        getMethodWithAuthorizationReturnJson(apiName: "my-profile/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                self.billingEmailTF = data["email"]?.string ?? ""
            }
        }
    }
    
    func ApiCallToBookProduct(){
        var params = [String:Any]()
        params["order_id"] = self.customerOrderId
        params["payment_method_id"] = self.paymentId
        params["payment_type_id"] = self.paymentgateway_type_id
        params["payment_method_name"] = self.paymentMode
        print(params)
        putMethodReturnJson(apiName: "checkout/", params: params, vc: self) { (response: JSON) in
            print(response)
            if response["status"].intValue == 200 {

                    let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let vc = storyboard.instantiateViewController(withIdentifier: "OrderPlacedViewController") as! OrderPlacedViewController
                    vc.orderType = "Payment"
                    vc.orderStatus = "Success"
                let orderId = response["order_id"].int ?? 0
                    vc.orderId = "\(orderId)"
                    if self.addressSelect == "yes" {
                        vc.addrDict = self.defaultAddressDict1
                    }
                    else {
                        vc.addrDict = self.paymentInfoDict
                    }
                    vc.subTotal =  self.lblSubTotal1.text!
                    vc.discount = self.lblDiscount.text!
                    vc.deliveryCharge =  self.lblDeliveryCharges.text!
                    vc.total = self.lblTotalAmount.text!
                   // self.PurchaseEvent(order_id : "\(orderId)")
                    self.navigationController?.pushViewController(vc, animated: true)
             //   }
            }
            else {
                let dictParam :[String:Any] = ["Order_id":"\(self.customerOrderId)"]
                print(dictParam)
                self.PurchaseFailedEvent(dictParam : dictParam)
                createalert(title: "Alert", message: response["message"].stringValue, vc: self)
                //self.showAlert32(message: response["message"].stringValue)
            }
            
        }
    }


//    func MakePayment() {
//        print(self.orderId)
//
//               // MARK:- Merchant Id Live/Demo
//              //  self.merchantIDTF = "45990" //Demo
//                  self.merchantIDTF = "46319" //Live
//
//                 // MARK:- Acces Key Live/Demo
//             //   self.acessCodeTF = "AVUP03GL28CI81PUIC" //Demo
//                  self.acessCodeTF = "AVZO03HA32BC46OZCB" //Live
//
//                  // MARK:- Currency Live/Demo
//                self.currencyTF = "AED"
//
//                // MARK:- Redirect url Live/Demo
//                //  self.redirectURLTF = "http://15.185.126.44:8062/api/front/v1/payment-res/" //Demo1
//              //    self.cancelURLTF = "http://15.185.126.44:8062/api/front/v1/payment-res/" //Demo1
//
//                self.redirectURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res/" //Live
//                self.cancelURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res/" //Live
//
//                paymentController = CCAvenuePaymentController.init(
//                                    orderId: self.merchant_param1,
//                                    merchantId: merchantIDTF,
//                                    accessCode: self.acessCodeTF,
//                                   // custId: custIDTF,
//                                    custId: self.merchant_param1,
//                                    amount: amountTF,
//                                    currency: "AED",
//                                    rsaKeyUrl: rsaKeyURLTF,
//                                    redirectUrl: redirectURLTF,
//                                    cancelUrl: cancelURLTF,
//                                    showAddress: "N",
//                                    billingName: billingNameTF,
//                                    billingAddress: billingAddressTF,
//                                    billingCity: billingCityTF,
//                                    billingState: billingStateTF,
//                                    billingCountry: billingCountryTF,
//                                    billingTel: billingTelTF,
//                                    billingEmail: billingEmailTF,
//                                    deliveryName: shippingNameTF,
//                                    deliveryAddress: shippingAddressTF,
//                                    deliveryCity: shippingCityTF,
//                                    deliveryState: shippingStateTF,
//                                    deliveryCountry: shippingCountry,
//                                    deliveryTel: shippingTelTF,
//                                    promoCode: " ",
//                                    merchant_param1: "\(self.orderId)",
//                                    merchant_param2: self.merchant_param2,
//                                    merchant_param3: "Paramater 3",
//                                    merchant_param4: "Paramater 4",
//                                    merchant_param5: "Paramater 5",
//                                    useCCPromo: " "
//                                )
//                    paymentController.delegate = self;
//                   self.present(paymentController, animated: true, completion: nil);
//    }
    
    
    func MakeDemoPayment() {
        
        
                       // MARK:- Merchant Id Live/Demo
                       self.merchantIDTF = "43366" //Demo
                       // self.merchantIDTF = "46319" //Live
        
                         // MARK:- Acces Key Live/Demo
                     self.acessCodeTF = "AVCG03HF47CJ43GCJC" //Demo
                      //  self.acessCodeTF = "AVZO03HA32BC46OZCB" //Live
        
                          // MARK:- Currency Live/Demo
                        self.currencyTF = "AED"
        
                        // MARK:- Redirect url Live/Demo
                         self.redirectURLTF = "http://15.185.126.44:8062/api/front/v1/payment-response/" //Demo1
                          self.cancelURLTF = "http://15.185.126.44:8062/api/front/v1/payment-response/" //Demo1
        
                      //  self.redirectURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res/" //Live
                     //   self.cancelURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res/" //Live
         //  self.rsaKeyURLTF = "https://www.gogrocery.ae/api/front/v1/get-rsa-demo/?order_id=\(self.orderId)" //Demo1
        self.rsaKeyURLTF = "https://www.gogrocery.ae/api/front/v1/get-rsa-demo/" //Demo1
        let paymentController = CCAvenuePaymentController.init(orderId:self.merchant_param1 ,
                                                               merchantId:self.merchantIDTF ,
                                                               accessCode:self.acessCodeTF,
                                                               custId:self.merchant_param1,
                                                               amount:"10.00",
                                                               currency:"AED",
                                                               rsaKeyUrl:self.rsaKeyURLTF,
                                                               redirectUrl:self.redirectURLTF,
                                                               cancelUrl:self.redirectURLTF,
                                                               showAddress:"Y",
                                                               billingName:"ABC",
                                                               billingAddress:"Star City",
                                                               billingCity:"Dubai",
                                                               billingState:"Dubai",
                                                               billingCountry:"United Arab Emirates",
                                                               billingTel:"+971 1234567890",
                                                               billingEmail:"test@gmail.com" ,
                                                               deliveryName:"XYZ",
                                                               deliveryAddress:"Internet City",
                                                               deliveryCity:"Dubai",
                                                               deliveryState:"Dubai",
                                                               deliveryCountry:"United Arab Emirates",
                                                               deliveryTel:"+971 9876543210",
                                                               promoCode:"" ,
                                                               merchant_param1:"Param 1",
                                                               merchant_param2:"Param 2",
                                                               merchant_param3:"Param 3",
                                                               merchant_param4:"Param 4" ,
                                                               merchant_param5:"Param 5",
                                                               useCCPromo:"Y",
                                                               siType:"ONDEMAND",
                                                               siMerchantRefNo:"1234",
                                                               siSetupAmount: "N",
                                                               siAmount: "1",
                                                               siStartDate: "20-07-2020",
                                                               siFrequencyType: "",
                                                               siFrequency: "",
                                                               siBillCycle: "")
         paymentController?.delegate = self;
         self.present(paymentController!, animated: true, completion: nil);
    }
    
       func ApicallToGetTransactionID() {
           var params = [String:Any]()
           params["order_id"] = self.customerOrderId
           postMethodQuery(apiName: "payment-transaction/", params: params, vc: self) { (response : JSON) in
               print(response)
               if response["status"].intValue == 0 {
                   let transactionDict = response["transaction_data"].dictionaryValue
                   self.orderIDTF = "\(transactionDict["custom_order_id"]!.int ?? 0)"
                   self.custIDTF = "\(transactionDict["customer_id"]!.int ?? 0)"
                   self.merchant_param1 = "\(transactionDict["custom_order_id"]!.string ?? "")"
                   self.merchant_param2 = "\(transactionDict["transaction_id"]!.int ?? 0)"
                   
                 //  self.rsaKeyURLTF = "https://www.gogrocery.ae/api/front/v1/get-rsa-demo/?order_id=\(self.orderIDTF)" //Demo
              //      self.rsaKeyURLTF = "http://15.185.126.44:8062/api/front/v1/get-rsa/?order_id=\(self.orderId)" //Demo1
                self.rsaKeyURLTF = "https://www.gogrocery.ae/api/front/v1/get-rsa-demo/?order_id=\(self.orderId)" //Demo1
                //self.rsaKeyURLTF = "https://www.gogrocery.ae/api/front/v1/get-rsa/?order_id=\(self.orderId)" //Live
               // self.MakePayment()
                 
               }
           }
       }
    
    func getResponse(_ responseDict_: NSMutableDictionary!)
    {
        // print(responseDict_)
        let orderNum = "\(responseDict_["order_id"] ?? "")"
        let orderStatus = "\(responseDict_["order_status"] ?? "")"
        print(orderStatus)
        let orderTrackId = "\(responseDict_["tracking_id"] ?? "")"
       //  if orderStatus == "Success" {
         let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
         let vc = storyboard.instantiateViewController(withIdentifier: "OrderPlacedViewController") as! OrderPlacedViewController
         //        let orderId = orderNum
         vc.orderId = self.customerOrderId
            vc.orderType = "Payment"
            vc.orderStatus = orderStatus
         if self.addressSelect == "yes" {
         vc.addrDict = self.defaultAddressDict1
         }
         else {
         vc.addrDict = self.paymentInfoDict
         }
         //        vc.addrDict = self.deafaultAddressDict
         vc.subTotal =  self.lblSubTotal1.text!
         vc.discount = self.lblDiscount.text!
         vc.deliveryCharge =  self.lblDeliveryCharges.text!
         vc.total = self.lblTotalAmount.text!
         // self.PurchaseEvent(order_id : self.customerOrderId)
//        let dictParam :[String:Any] = ["Content_ID":"\(self.customerOrderId)","Currency": "AED", "ValueToSum":"\(self.lblTotalAmount.text!)"]
//        print(dictParam)
//        self.PurchaseEvents(dictParam: dictParam)
         self.navigationController?.pushViewController(vc, animated: true)
        // }
            
//         else {
//         let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
//         let vc = storyboard.instantiateViewController(withIdentifier: "PaymentFailedViewController") as! PaymentFailedViewController
//         self.navigationController?.pushViewController(vc, animated: true)
//
//         }
//
    }
    
    func ApiCallToGetPaymentMethod() {
        let auth = UserDefaults.standard.value(forKey: "token") as! String
       // let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        let headers:[String : Any] = ["Authorization": "Token \(auth)", "Content-Type": "application/json"]
        
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "payment-method/", vc: self, header: headers) { (response : JSON) in
            print(response)
            self.paymentMethodArr = response["api_status"].arrayValue
            self.viewPaymentHeight.constant = CGFloat(50*self.paymentMethodArr.count)
            self.tableView.dataSource = self
            self.tableView.delegate = self
            self.tableView.reloadData()
        }
    }
    
    //MARK:- Events
      func PurchaseEvents(dictParam : [String:Any]) {
        Analytics.logEvent("purchase_events", parameters: dictParam)
    }
    func PurchaseFailedEvent(dictParam : [String:Any]) {
         Analytics.logEvent("PurchaseFailed", parameters: dictParam)
     }
    //MARK:- Alert Showing
    func showAlertOnOrderInfo(message: String)
        {
            let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
                self.navigationController?.popViewController(animated: true)
                
            }))
            self.present(alert, animated: true, completion: nil)
        }
}
extension CCPaymentViewController : UITableViewDataSource , UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.paymentMethodArr.count
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        50
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
         let cell = Bundle.main.loadNibNamed("PaymentMethodTableViewCell", owner: self, options: nil)?.first as! PaymentMethodTableViewCell
        let dict = self.paymentMethodArr[indexPath.row].dictionaryValue
        let dict1 = dict["engageboost_paymentgateway_method_id"]?.dictionaryValue
        self.paymentId = dict1?["id"]?.int ?? 0
        cell.lblPaymentType.text = dict1?["name"]?.string ?? ""
        if self.paymentIdArr.contains( self.paymentId) {
             cell.imgImage.image = UIImage(named: "radio_select")
         }
         else {
             cell.imgImage.image = UIImage(named: "radio_unselect")
         }
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let dict = self.paymentMethodArr[indexPath.row].dictionaryValue
        let dict1 = dict["engageboost_paymentgateway_method_id"]?.dictionaryValue
        self.paymentId = dict1?["id"]?.int ?? 0
        self.paymentgateway_type_id = dict1?["paymentgateway_type_id"]?.int ?? 0
        self.paymentIdArr.removeAll()
        //self.tableView.reloadRows(at: [indexPath], with: UITableView.RowAnimation.none)
        self.paymentIdArr.append(self.paymentId)
        self.paymentMode = dict1?["name"]?.string ?? ""
        self.tableView.reloadData()
       // self.tableView.reloadRows(at: [indexPath], with: UITableView.RowAnimation.none)
        print("Payment ID ------------->>>>>>>>>>>>> \(self.paymentId)")
        print("Payment Gateway ID ------------->>>>>>>>>>>>> \(self.paymentgateway_type_id)")
    }
}
