//
//  DeliveryDetailsViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 30/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import DropDown
import SwiftyJSON
import FirebaseAnalytics
import CCAvenueSDK
class DeliveryDetailsViewController: UIViewController , UITextFieldDelegate ,CCAvenuePaymentControllerDelegate{
    
    @IBOutlet weak var viewDeliveryAddress: UIView!
    @IBOutlet weak var viewDeliveryData: UIView!
    @IBOutlet weak var viewDeliveryoptions: UIView!
    @IBOutlet weak var viewDeliverySlot: UIView!
    @IBOutlet weak var viewPromo: UIView!
    @IBOutlet weak var viewLoyalty: UIView!
    @IBOutlet weak var viewWalletBalance: UIView!
    @IBOutlet weak var viewOrderSummary: UIView!
    @IBOutlet weak var viewAmount: UIView!
    @IBOutlet weak var viewTotalAmpont: UIView!
    @IBOutlet weak var viewChoosSlot: UIView!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var lblApartment: UILabel!
    @IBOutlet weak var lblCountry: UILabel!
    @IBOutlet weak var lblMobile: UILabel!
    @IBOutlet weak var btnChangeOrAddAddress: UIButton!
    @IBOutlet weak var btnDeliverySlot: UIButton!
    @IBOutlet weak var lblWalletBalance: UILabel!
    @IBOutlet weak var lblSubTotal: UILabel!
    @IBOutlet weak var lblDefault: UILabel!
    @IBOutlet weak var lblDeliverySlot: UILabel!
    @IBOutlet weak var lblDiscount: UILabel!
    @IBOutlet weak var lblDeliveryCharges: UILabel!
    @IBOutlet weak var lblTotalAmount: UILabel!
    @IBOutlet weak var lblSubtotal: UILabel!
    @IBOutlet weak var btnContinue: UIButton!
    @IBOutlet weak var viewContinue: UIView!
    @IBOutlet weak var btnDelete: UIButton!
    @IBOutlet weak var lblPromoCode: UILabel!
    @IBOutlet weak var lblAppliedWalletAmount: UILabel!
    @IBOutlet weak var lblAppliedWallet: UILabel!
    @IBOutlet weak var lblWallet: UILabel!
    @IBOutlet weak var btnWalletCheck: UIButton!
    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var viewPaymentHeight: NSLayoutConstraint!
    @IBOutlet weak var viewPayment: UIView!
    @IBOutlet weak var blankView: UIView!
    
    var paymentMethodArr = [JSON]()
    var cartSumDict = [String:JSON]()
    var minimum_order_amount = Int()
    var minimum_order_amount_check = String()
    var addressId = Int()
    var addressArray = [JSON]()
    var deafaultAddressDict = [String:JSON]()
    var defaultAddressDict = [String:JSON]()
    var addressSelect = String()
    var ruleId = Int()
    var addressID = Int()
    var timeSlotDate = String()
    var timeSlotTime = String()
    var deliverySlotArr = [JSON]()
    var deliveryDateArr = [String]()
    var deliverTimeArr = [[String:String]]()
    var deliverDayArr = [String]()
    var walletBalance:Int = 0
    var walletUsableBalance:Int = 0
    var walletCheck:Bool = false
    var couponString:String = ""
    var wBalance:Int = 0
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var contentNameArray = [String]()
    var contentIdArray = [String]()
    var skuArray = [String]()
    var quantArray = [String]()
    var contentNames = String()
    var contentIds = String()
    var skus = String()
    var quants = String()
    var mustArray = [[String:Any]]()
    var customInfoDict = [String:Any]()
    var cartArrayCount = Int()
    var paymentMode:String = ""
    var paymentId = Int()
    var paymentgateway_type_id = Int()
    var paymentIdArr = [Int]()
    var paymentSelectIndex = 9999
    var paymentMethodName = String()
    var cartCount = Int()
    
    //MARK:- Payment Outlet Declaration
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
    var customerOrderId = String()
    var paymentStatusFromPlaced = String()
    var orderIdFromPlaced = String()
    // MARK: - View lifecycle
    // MARK: -
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        viewContinue.addShadow1()
        self.navigationView.addShadow1()
        self.couponString = ""
        viewDeliveryData.addShadow1()
        viewDeliverySlot.addShadow1()
        viewPayment.addShadow1()
        viewPromo.addShadow1()
        viewWalletBalance.addShadow1()
        viewAmount.addShadow1()
        viewTotalAmpont.addShadow1()
        viewContinue.addShadow1()
        viewChoosSlot.layer.cornerRadius = 5
        viewChoosSlot.layer.borderColor = UIColor.darkGray.cgColor
        viewChoosSlot.layer.borderWidth = 1
        btnChangeOrAddAddress.layer.cornerRadius = 5
        btnChangeOrAddAddress.addShadow1()
        self.lblDefault.layer.cornerRadius = self.lblDefault.frame.height/2
        self.lblDefault?.layer.masksToBounds = true
        self.btnContinue.layer.cornerRadius = 5
        self.btnContinue.addShadow1()
        self.btnDelete.isHidden = true
        ApiCallToGetDeliverySlot()
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.blankView.isHidden = true
        self.btnContinue.isUserInteractionEnabled = true
        contentNameArray.removeAll()
        contentIdArray.removeAll()
        skuArray.removeAll()
        quantArray.removeAll()
        mustArray.removeAll()
        self.paymentIdArr.removeAll()
        self.paymentId = 0
        self.paymentgateway_type_id = 0
        self.paymentSelectIndex = 9999
        self.paymentMethodArr.removeAll()
        self.tableView.reloadData()
        self.ApiCallToGetPaymentMethod()
        self.navigationController?.isNavigationBarHidden = true
        if addressSelect == "yes" {
            deafaultAddressDict = defaultAddressDict
            DiplayDefaultAddress()
            ApiCallToGetCartSummary()
        }
        else {
            ApiCallToGetAddressList()
            ApiCallToGetCartSummary()
        }
    }
    //    MARK:- Dropdown SetUP
    let MonthDropDown = DropDown()
    lazy var dropDowns: [DropDown] = {
        return [
            self.MonthDropDown,
        ]
    }()
    func setupDropDowns() {
        self.setupMonthDropDown()
    }
    func setupMonthDropDown() {
        MonthDropDown.anchorView = viewChoosSlot
        MonthDropDown.bottomOffset = CGPoint(x: 0, y: 50)
        MonthDropDown.dataSource = self.deliverDayArr
        if self.deliverDayArr[0] == "SameDay" || self.deliverDayArr[0] == "Sameday" || self.deliverDayArr[0] == "sameday" || self.deliverDayArr[0] == "sameDay" || self.deliverDayArr[0] == "Same Day"{
            self.lblDeliverySlot.text = "Same Day"
        }
        if self.deliverDayArr[0] == "Nextday" || self.deliverDayArr[0] == "NextDay" || self.deliverDayArr[0] == "nextday" || self.deliverDayArr[0] == "nextDay" || self.deliverDayArr[0] == "Next Day" {
            self.lblDeliverySlot.text = "Next Day"
        }
        self.timeSlotDate = self.deliveryDateArr[0]
        let dict = self.deliverTimeArr[0]
        self.timeSlotTime = "\(dict["start_time"]!)-\(dict["end_time"]!)"
//        print(self.timeSlotDate)
//        print(self.timeSlotTime)
//        print(self.deliverDayArr[0])
        
        // Action triggered on selection
        MonthDropDown.selectionAction = { [weak self] (index, item) in
            self!.lblDeliverySlot.text = ""
            self!.lblDeliverySlot.text = item
            if item == "SameDay" || item == "Sameday" || item == "sameday" {
                self?.lblDeliverySlot.text = "Same Day"
            }
            if item == "Nextday" || item == "NextDay" || item == "nextday" {
                self?.lblDeliverySlot.text = "Next Day"
            }
            self!.timeSlotDate = self!.deliveryDateArr[index]
            let dict = self!.deliverTimeArr[index]
            self?.timeSlotTime = "\(dict["start_time"]!)-\(dict["end_time"]!)"
//            print(self!.timeSlotDate)
//            print(self!.timeSlotTime)
//            print(self!.deliverDayArr[index])
            self!.MonthDropDown.hide()
            
        }
        MonthDropDown.multiSelectionAction = { [weak self] (indices, items) in
            print("Muti selection action called with: \(items)")
            if items.isEmpty {
                self?.lblDeliverySlot.text = ""
            }
        }
    }
    
    func  DiplayDefaultAddress() {
        if deafaultAddressDict.isEmpty == false {
            self.lblName.text = deafaultAddressDict["delivery_name"]!.string ?? ""
            self.lblApartment.text = deafaultAddressDict["delivery_street_address"]!.string ?? "" + " " + (deafaultAddressDict["billing_landmark"]!.string ?? "")
            self.lblCountry.text = deafaultAddressDict["delivery_state_name"]!.string ?? "" + " " + (deafaultAddressDict["delivery_country_name"]!.string ?? "")
            self.lblMobile.text = deafaultAddressDict["delivery_phone"]!.string ?? ""
            self.addressId = deafaultAddressDict["id"]!.int ?? 0
            ApiCallToGetCartSummary()
        }
        else {
            ApiCallToGetAddressList()
        }
    }
    
    @IBAction func btnBackAction(_ sender: Any) {
        if let viewControllers = self.navigationController?.viewControllers
        {
            for aViewController in viewControllers {
                if aViewController is CartViewController {
                    self.navigationController?.popToViewController(aViewController, animated: true)
                }
            }
        }
    }
    
    @IBAction func btnAddOrChangeAddressAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "SavedAdressListViewController") as! SavedAdressListViewController
        vc.pageTypeFromCheckOut = "CheckOut"
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnDeliverySlotAction(_ sender: Any) {
        MonthDropDown.show()
    }
    @IBAction func btnContinueAction(_ sender: Any) {
        if timeSlotDate.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please select delivery slot", vc: self)
        }
        else  if timeSlotTime.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please select delivery slot", vc: self)
        }
      else if paymentMode.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please select Payment Method", vc: self)
        }
       else if self.paymentId == 0 {
          createalert(title: "Alert", message: "Please select Payment Method", vc: self)
        }
        else {
            self.btnContinue.isUserInteractionEnabled = false
            ApiCallToCheckAddress()
        }
    }
    
    @IBAction func btnPromoAction(_ sender: Any) {
        setUpPromoXibFunc()
    }
    
    @IBAction func btnDeleteAction(_ sender: Any) {
        promoXib.txtPromo.text = ""
        self.btnDelete.isHidden = true
        ApiCallToApplyPromoCode()
    }
    
    @IBAction func btnWalletCheckAction(_ sender: Any) {
        if walletCheck == false {
            btnWalletCheck.setImage(UIImage(named: "checkbox_select"), for: .normal)
            walletCheck = true
            walletUsableBalance = wBalance
           // ApiCallToApplyWalletBalance()
        }
        else {
            btnWalletCheck.setImage(UIImage(named: "checkbox_unselect"), for: .normal)
            walletCheck = false
            walletUsableBalance = 0
            ApiCallToApplyWalletBalance()
        }
    }
    
    //    MARK:- Sorting Xib
    func setUpPromoXibFunc () {
        requestPromoView(vc: self)
        promoXib.btnPrompApply.addTarget(self, action: #selector(btnPromoApplyAction), for: .touchUpInside)
        promoXib.txtPromo.delegate = self
        promoXib.btnPrompApply.layer.cornerRadius = 5
        promoXib.btnPrompApply.addShadow1()
        promoXib.btnCancel.layer.cornerRadius = 5
        promoXib.btnDismissPromo.addTarget(self, action: #selector(btnDismissPromoAction), for: .touchUpInside)
        promoXib.btnCancel.addTarget(self, action: #selector(btnCancelAction), for: .touchUpInside)
        promoXib.btnCancel.layer.cornerRadius = promoXib.btnCancel.frame.height/2
        promoXib.promoView.layer.shadowColor = UIColor.lightGray.cgColor
        promoXib.promoView.layer.shadowOpacity = 1
        promoXib.promoView.layer.shadowOffset = .zero
        promoXib.promoView.layer.cornerRadius = 5
        promoXib.promoView.layer.shadowRadius = 1
        promoXib.promoView.layer.shadowPath = UIBezierPath(rect: promoXib.promoView.bounds).cgPath
        promoXib.promoView.layer.shouldRasterize = true
        promoXib.promoView.layer.rasterizationScale = UIScreen.main.scale
        promoXib.promoView.addShadow1()
        promoXib.txtPromo.layer.cornerRadius = 5
        promoXib.txtPromo.setLeftPaddingPoints(10)
        promoTxtInActive()
    }
    
    //    MARK:- Active
    func promoTxtActive() {
        promoXib.txtPromo.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        promoXib.txtPromo.layer.borderWidth = 1
        promoXib.lblPromo.isHidden = false
    }
    //    MARK:- InActive
    func promoTxtInActive() {
        promoXib.txtPromo.layer.borderColor = UIColor.darkGray.cgColor
        promoXib.txtPromo.layer.borderWidth = 1
        promoXib.lblPromo.isHidden = true
    }
    
    @objc func btnPromoApplyAction() {
        //promoXib.removeFromSuperview()
        ApiCallToApplyPromoCode()
    }
    
    @objc func btnDismissPromoAction() {
        promoXib.removeFromSuperview()
    }
    
    @objc func btnCancelAction() {
        promoXib.removeFromSuperview()
    }
    
    //    MARK:- TextField delegate
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == promoXib.txtPromo {
            promoTxtActive()
        }
    }
    
    func textFieldDidEndEditing(_ textField: UITextField, reason: UITextField.DidEndEditingReason) {
        if textField == promoXib.txtPromo {
            promoTxtInActive()
        }
    }
    
    //    MARK:- Api Calling
    
    func ApiCallToCheckAddress() {
        var params = [String:Any]()
        params["address_id"] = self.addressId
        var headers = [String : Any]()
        let auth = UserDefaults.standard.value(forKey: "token") as? String ?? ""
        headers = ["Authorization": "Token \(auth)","Content-Type": "application/json" , "WAREHOUSE" : "\(wareHouseId)","WID":"1"]
        postMethodCustomHeader(apiName: "select-address/", params: params, vc: self, header: headers) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                if response["warehouseMatch"].stringValue == "y" {
                    self.btnContinue.isUserInteractionEnabled = false
                     self.ApiCallToBookProduct()
//                    if self.paymentStatusFromPlaced == "Failed"{
//                        self.ApiCallToBookProduct()
//                        //self.ApicallToGetTransactionID()
//                    }
//                     else {
//                       self.ApiCallToBookProduct()
//                    }
                    
                }
                else {
                    self.btnContinue.isUserInteractionEnabled = true
                    createalert(title: "Alert", message: response["message"].string ?? "", vc: self)
                }
            }
            else {
            }
        }
    }
    
    func ApiCallToBookProduct() {
        let specialInstructions = UserDefaults.standard.value(forKey: "addNote") as? String ?? ""
        var promoString: String = ""
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as? Int ?? 0
        if self.couponString.trimmingCharacters(in: .whitespaces).isEmpty{
            promoString = ""
        }
        else {
            promoString = self.couponString
        }
        var params = [String:Any]()
        params["address_book_id"] = self.addressId
        params["time_slot_date"] = timeSlotDate
        params["time_slot_time"] = timeSlotTime
        params["special_instruction"] = specialInstructions
        params["coupon_code"] = promoString
        if walletCheck == false {
            self.walletUsableBalance = 0
        }
        else {
            self.walletUsableBalance = wBalance
        }
        params["redeem_amount"] = self.walletUsableBalance
        params["rule_id"] = ruleId
        params["website_id"] = 1
        params["device_id"] = deviceID
        params["warehouse_id"] = wareHouseId
        params["webshop_id"] = 33
        params["payment_method_id"] = self.paymentId
        params["payment_type_id"] = self.paymentgateway_type_id
        params["payment_method_name"] = self.paymentMode
       // let api = "save-cart-si/" //LIVE
        let api = "save-cart/" //DEMO
        postMethodQuery2(apiName: api, params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "OrderPlacedViewController") as! OrderPlacedViewController
                let orderId = response["order_id"].string ?? "0"
                vc.orderId = "\(orderId)"
                self.customerOrderId = orderId
//                vc.orderType = "Payment"
                vc.orderStatus = "Success"
                let orderData = response["order_data"].dictionaryValue
                let customerInfoDict = orderData["customer_info"]?.dictionaryValue
                vc.addrDict = customerInfoDict ?? [String:JSON]()
                self.deafaultAddressDict = customerInfoDict ?? [String:JSON]()
                self.getAddressFromApiCall()
                vc.subTotal =  self.lblSubTotal.text!
                vc.discount = self.lblDiscount.text!
                vc.deliveryCharge =  self.lblDeliveryCharges.text!
                vc.total = self.lblTotalAmount.text!
                
               // let customInfoDictt = ["name":customerInfoDict!["delivery_name"]!.stringValue ,"email": customerInfoDict!["delivery_email_address"]!.stringValue,"billing_name":customerInfoDict!["delivery_name"]!.stringValue,"delivery_name":customerInfoDict!["delivery_name"]!.stringValue]
                
                let customInfoDictt = ["name":customerInfoDict!["delivery_name"]!.stringValue ,"email": customerInfoDict!["delivery_email_address"]!.stringValue]
                let checkOutItemNamesWithQauntity :[String:Any] = ["orderId": "\(orderId)", "OrderFrom":"IOS","item_items": self.mustArray,"customer" :customInfoDictt]

                let content_ids = self.contentIdArray // all productId [ 1, 2 ,3 ]
                let content_name = self.contentNameArray // all product Name
              //  let contents = self.contentNameArray //
                let content_type = "product_group"
                let num_items = self.cartCount
                let value = self.lblSubTotal.text // orde total
                let currency = "AED"
                let dictParam :[String:Any] = ["content_ids":content_ids,"content_name":content_name,"contents":checkOutItemNamesWithQauntity,"content_type":content_type,"num_items":num_items,"Value_To_Sum":value!,"currency":currency]
                
                print(dictParam)
                PlaceOrder(dictParam: dictParam)
                
                let requiredJson: [String: Any]  = ["orderId":vc.orderId , "OrderFrom" : "IOS", "item_items" : self.mustArray, "customer" : self.customInfoDict]// Demo
                logAddPaymentInfoEvent(contentIds: self.contentIds, contentName: self.contentNames, contentType: "product_group", numItems: "\(self.cartArrayCount)", value: vc.total, currency: "AED", contents: requiredJson)
                self.btnContinue.isUserInteractionEnabled = false
                if self.paymentMode == "Credit / Debit Card(Online Payment)" {
                    self.ApicallToGetTransactionID()
                }
                else {
                    self.navigationController?.pushViewController(vc, animated: true)
                }
                
            }
            else {
                self.btnContinue.isUserInteractionEnabled = true
                self.showAlert32(message: response["message"].stringValue)
            }
        }
    }
    func ApiCallToGetAddressList() {
        getMethodWithAuthorizationReturnJsonWithoutDeviceId(apiName: "delivery-address/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.addressArray = response["data"].arrayValue
                if self.addressArray.count != 0 {
                    for i in 0...self.addressArray.count - 1 {
                        let addressDict = self.addressArray[i].dictionaryValue
                        // if addressDict["set_primary"]!.intValue == 1 {
                        self.deafaultAddressDict = addressDict
                        self.DiplayDefaultAddress()
                        // }
                    }
                }
                else {
                    let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let vc = storyboard.instantiateViewController(withIdentifier: "SaveAddressViewController") as! SaveAddressViewController
                    vc.pageType = "Add"
                    vc.pageTypeFrom = "Cart"
                    //  vc.pageTypeFromCheckOut = "noCheckout"
                    self.navigationController?.pushViewController(vc, animated: true)
                }
            }
            else {
                let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "SaveAddressViewController") as! SaveAddressViewController
                vc.pageType = "Add"
                vc.pageTypeFrom = "Cart"
                //  vc.pageTypeFromCheckOut = "noCheckout"
                self.navigationController?.pushViewController(vc, animated: true)
                //                createalert(title: "Alert", message: response["message"].stringValue, vc: self)
            }
        }
    }
    
    func  ApiCallToGetCartSummary() {
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        var params = [String:Any]()
        params["warehouse_id"] = wareHouseId
        // params["address_id"] = self.addressID
        params["address_id"] = ""
        params["coupon_code"] = ""
        postMethodQuery2(apiName: "cart-summary/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                let cartData = response["data"].dictionaryValue
                self.cartArrayCount = (cartData["cartdetails"]?.arrayValue.count)!
                let cartDetailsArr = cartData["cartdetails"]?.arrayValue
                self.cartCount = cartData["cart_count"]?.intValue ?? 0
                for index in cartDetailsArr! {
                    
                    let contentName = index["name"].stringValue
                    self.contentNameArray.append(contentName)
                    self.contentNames = self.contentNames + contentName + ", "
                    
                    let contentId = "\(index["id"].intValue)"
                    self.contentIdArray.append(contentId)
                    self.contentIds = self.contentIds  + contentId + ", "
                    
                    let sku = index["sku"].stringValue
                    self.skus = self.skus  + sku + ", "
                    self.skuArray.append(sku)
                    
                    let quant = "\(index["qty"].intValue)"
                    self.quantArray.append(quant)
                    
                    let dict = ["ID":contentId,"SKU":sku,"QUANTITY":quant]
                    self.mustArray.append(dict)
                    
                }
                
                
                self.minimum_order_amount = response["minimum_order_amount"].int ?? 0
                self.minimum_order_amount_check = response["minimum_order_amount_check"].string ?? ""
                self.ruleId = response["rule_id"].int ?? 0
                self.cartSumDict = response["data"].dictionaryValue
                let orderamountdetailsArr = self.cartSumDict["orderamountdetails"]?.arrayValue
                let orderamountdetailsDict = orderamountdetailsArr![0].dictionaryValue
                let loyalityDict = self.cartSumDict["loyalty_details"]?.dictionaryValue
                if loyalityDict!["remain_loyalty"]!.int ?? 0 != 0 {
                    let remainLoyality = loyalityDict!["remain_loyalty"]!.int ?? 0
                    self.walletBalance = remainLoyality
                    self.lblWalletBalance.text = "Wallet Balance - AED \(remainLoyality)"
                    self.walletUsableBalance = loyalityDict!["usable_loyalty"]!.int ?? 0
                    self.wBalance = loyalityDict!["usable_loyalty"]!.int ?? 0
                    self.lblWallet.isHidden = false
                    //                self.walletUsableBalance = walletUsableBalance
                    self.lblWallet.text = "You can use upto AED \(loyalityDict!["usable_loyalty"]!.int ?? 0) for this order"
                    self.btnWalletCheck.isHidden = false
                }
                else {
                    self.btnWalletCheck.isHidden = true
                    self.lblWallet.isHidden = true
                    //  self.lblWallet.text = "Your Wallet Balance is AED 0"
                    self.lblWalletBalance.text = "Wallet Balance - AED 0.00 "
                }
                print(orderamountdetailsDict)
                let tt = orderamountdetailsDict["sub_total"]!.float ?? 0.00
                print(tt)
                let st = String(format: "%.2f", tt)
                print(st)
                self.lblSubTotal.text = "AED \(st)"
                
                let ct = orderamountdetailsDict["cart_discount"]!.float ?? 0.00
                let ctt = String(format: "%.2f", ct)
                self.lblDiscount.text = "AED \(ctt)"
                
                let ld = orderamountdetailsDict["shipping_charge"]!.float ?? 0.00
                let ldd = String(format: "%.2f", ld)
                self.lblDeliveryCharges.text = "AED \(ldd)"
                
                let ta = orderamountdetailsDict["grand_total"]!.float ?? 0.00
                let taa = String(format: "%.2f", ta)
                self.lblTotalAmount.text = "AED \(taa)"
                
                let tss = orderamountdetailsDict["grand_total"]!.float ?? 0.00
                let tsst = String(format: "%.2f", tss)
                self.lblSubtotal.text = "AED \(tsst)"
                self.amountTF = tsst
                self.getAddressFromApiCall()
            }
            else {
                createalert(title: "Alert", message: response["msg"].string ?? "", vc: self)
            }
        }
    }
    
    func ApiCallToGetDeliverySlot() {
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as? Int ?? 0
        getMethodWithAuthorizationReturnJsonwithWareHouseId(apiName: "delivery-slot/\(wareHouseId)/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 1 {
                self.deliverySlotArr = response["delivery_slot"].arrayValue
                for i in 0...self.deliverySlotArr.count - 1 {
                    let deliverySlotDict = self.deliverySlotArr[i].dictionaryValue
                    self.deliveryDateArr.append(deliverySlotDict["delivery_date"]!.string ?? "")
                    let tempArr = deliverySlotDict["available_slot"]?.arrayValue
                    let tempDict = tempArr![0].dictionaryValue
                    let startTime = tempDict["start_time"]?.string ?? ""
                    let endTime = tempDict["end_time"]!.string ?? ""
                    let tempTimeDict = ["start_time":startTime,"end_time":endTime]
                    self.deliverTimeArr.append(tempTimeDict as! [String : String])
                    let dayString = tempDict["based_on"]!.stringValue
                    // self.deliverDayArr.append(dayString)
                    if dayString == "SameDay" || dayString == "Sameday" || dayString == "sameday" || dayString == "sameDay"{
                        self.deliverDayArr.append("Same Day")
                    }
                    if dayString == "Nextday" || dayString == "NextDay" || dayString == "nextday" || dayString == "nextDay" {
                        self.deliverDayArr.append("Next Day")
                    }
                    self.setupDropDowns()
                }
            }
            else {
                createalert(title: "Alert", message: "Unable to fetch delivery slot", vc: self)
            }
            
        }
    }
    
    func ApiCallToApplyPromoCode() {
        var params = [String:Any]()
        self.couponString = promoXib.txtPromo.text!
        params["coupon_code"] = promoXib.txtPromo.text!
        postMethodQueryApplyCoupon(apiName: "apply-coupon/", params: params, vc: self) { (response: JSON) in
            print(response)
            if response["status"].intValue == 200 {
                let cartDict = response["data"].dictionaryValue
                let orderamountdetailsArr = cartDict["orderamountdetails"]?.arrayValue
                let orderamountdetailsDict = orderamountdetailsArr![0].dictionaryValue
                print(orderamountdetailsDict)
                
                let st = orderamountdetailsDict["sub_total"]!.float ?? 0.00
                let stt = String(format: "%.2f", st)
                self.lblSubTotal.text = "AED \(stt)"
                
                let ct = orderamountdetailsDict["cart_discount"]!.float ?? 0.00
                let ctt = String(format: "%.2f", ct)
                self.lblDiscount.text = "AED \(ctt)"
                
                let ld = orderamountdetailsDict["shipping_charge"]!.float ?? 0.00
                 let ldd = String(format: "%.2f", ld)
                self.lblDeliveryCharges.text = "AED \(ldd)"
                
                let ta = orderamountdetailsDict["grand_total"]!.float ?? 0.00
                 let taa = String(format: "%.2f", ta)
                self.lblTotalAmount.text = "AED \(taa)"
                
                let tss = orderamountdetailsDict["grand_total"]!.float ?? 0.00
                let tsst = String(format: "%.2f", tss)
                self.lblSubtotal.text = "AED \(tsst)"
                if cartDict["applied_coupon"]?.arrayValue.count != 0 {
                    let applied_couponArr = cartDict["applied_coupon"]?.arrayValue
                    let applied_couponDict = applied_couponArr![0].dictionaryValue
                    let message = applied_couponDict["name"]!.string ?? ""
                    if message != "invalid" {
                        promoXib.removeFromSuperview()
                        self.lblPromoCode.text = "You have saved AED \(ctt)"
                        self.btnDelete.isHidden = false
                    }
                    else {
                        promoXib.removeFromSuperview()
                        self.btnDelete.isHidden = true
                        createalert(title: "Alert", message: applied_couponDict["message"]!.string ?? "", vc: self)
                        //  self.setUpPromoXibFunc()
                    }
                }
                else {
                    self.btnDelete.isHidden = true
                    self.lblPromoCode.text = "Apply Promo Code"
                }
            }
        }
    }
    
    func ApiCallToApplyWalletBalance() {
        var params = [String:Any]()
        params["redeem_amount"] = walletUsableBalance
        print(params)
        postMethodQueryApplyCoupon(apiName: "apply-coupon/", params: params, vc: self) { (response: JSON) in
            print(response)
            if response["status"].intValue == 200 {
                let cartDict = response["data"].dictionaryValue
                self.btnDelete.isHidden = false
                let orderamountdetailsArr = cartDict["orderamountdetails"]?.arrayValue
                let orderamountdetailsDict = orderamountdetailsArr![0].dictionaryValue
                print(orderamountdetailsDict)
                
                let st = orderamountdetailsDict["sub_total"]!.float ?? 0.00
                let stt =   String(format: "%.2f", st)
                self.lblSubTotal.text = "AED \(stt)"
                
                let ct = orderamountdetailsDict["cart_discount"]!.float ?? 0.00
                let ctt = String(format: "%.2f", ct)
                self.lblDiscount.text = "AED \(ctt)"
                
                let ld = orderamountdetailsDict["shipping_charge"]!.float ?? 0.00
                let ldd = String(format: "%.2f", ld)
                self.lblDeliveryCharges.text = "AED \(ldd)"
                
                let ta = orderamountdetailsDict["grand_total"]!.float ?? 0.00
                let taa = String(format: "%.2f", ta)
                self.lblTotalAmount.text = "AED \(taa)"
                
                let tss = orderamountdetailsDict["grand_total"]!.float ?? 0.00
                let tsst = String(format: "%.2f", tss)
                self.lblSubtotal.text = "AED \(tsst)"
                
                if  let applied_loyalty_amount = orderamountdetailsDict["applied_loyalty_amount"]?.float {
                     let taa = String(format: "%.2f", applied_loyalty_amount)
                    self.lblAppliedWalletAmount.text = "AED \(taa)"
                    self.lblAppliedWallet.isHidden = false
                    self.lblAppliedWalletAmount.isHidden = false
                }
                else {
                    self.lblAppliedWallet.isHidden = true
                    self.lblAppliedWalletAmount.isHidden = true
                }
                if cartDict["applied_coupon"]?.arrayValue.count != 0 {
                    let applied_couponArr = cartDict["applied_coupon"]?.arrayValue
                    let applied_couponDict = applied_couponArr![0].dictionaryValue
                    let message = applied_couponDict["name"]!.string ?? ""
                    if message != "invalid" {
                        promoXib.removeFromSuperview()
                        self.lblPromoCode.text = "You have saved AED \(ctt)"
                    }
                    else {
                        let message1 = applied_couponDict["message"]!.string ?? ""
                        createalert(title: "Alert", message: message1, vc: self)
                    }
                }
                else {
                    self.btnDelete.isHidden = true
                    self.lblPromoCode.text = "Apply Promo Code"
                }
            }
        }
    }
    
    func ApiCallToGetPaymentMethod() {
        let auth = UserDefaults.standard.value(forKey: "token") as? String ?? ""
         let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        let headers:[String : Any] = ["Authorization": "Token \(auth)", "Content-Type": "application/json",  "WAREHOUSE": "\(wareHouseId)"]
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "payment-method/", vc: self, header: headers) { (response : JSON) in
            print(response)
            self.paymentMethodArr = response["api_status"].arrayValue
            self.viewPaymentHeight.constant = CGFloat(40*self.paymentMethodArr.count) + 1
            self.tableView.dataSource = self
            self.tableView.delegate = self
            self.tableView.reloadData()
        }
    }
    
    func MakeDemoPayment() {
        let date = Date()
        let formatter = DateFormatter()
        formatter.dateFormat = "dd-MM-yyyy"
        let result = formatter.string(from: date)
        let dateToday = result
        // label.text = result
        // MARK:- Merchant Id Live/Demo
        self.merchantIDTF = "43366" //Demo
      //   self.merchantIDTF = "46319" //Live
        
        // MARK:- Acces Key Live/Demo
        self.acessCodeTF = "AVCG03HF47CJ43GCJC" //Demo
        //  self.acessCodeTF = "AVZO03HA32BC46OZCB" //Live
        
        // MARK:- Currency Live/Demo
        self.currencyTF = "AED"
        
     //        MARK:- Redirect and Cancel Url for Demo
        
        self.redirectURLTF =  baseUrl + "payment-res-demo/"
        self.cancelURLTF = baseUrl + "payment-res-demo/"
       // payment-response/
        
//        self.redirectURLTF =  baseUrl + "payment-response/"
//        self.cancelURLTF = baseUrl + "payment-response/"
       
//        MARK:- Redirect and Cancel Url for live
      //  self.redirectURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res-si/"
       // self.cancelURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res-si/"

        print(self.redirectURLTF)
        let paymentController = CCAvenuePaymentController.init(orderId:self.merchant_param1 ,
            merchantId:self.merchantIDTF ,
            accessCode:self.acessCodeTF,
            custId:self.merchant_param1,
            //  amount:amountTF,
            amount:"1",
            currency:"AED",
            rsaKeyUrl:self.rsaKeyURLTF,
            redirectUrl:self.redirectURLTF,
            cancelUrl:self.redirectURLTF,
            showAddress:"N",
            billingName:billingNameTF,
            billingAddress:billingAddressTF,
            billingCity:billingCityTF,
            billingState:billingStateTF,
            billingCountry:billingCountryTF,
            billingTel:billingTelTF,
            billingEmail:billingEmailTF ,
            deliveryName:shippingNameTF,
            deliveryAddress:shippingAddressTF,
            deliveryCity:shippingCityTF,
            deliveryState:billingStateTF,
            deliveryCountry:billingCountryTF,
            deliveryTel:billingTelTF,
            promoCode:"" ,
            merchant_param1:self.merchant_param1,
            merchant_param2:self.merchant_param2,
            merchant_param3:"Param 3",
            merchant_param4:"Param 4" ,
            merchant_param5:"Param 5",
            useCCPromo:"Y",
            siType:"ONDEMAND",
            siMerchantRefNo:"",
            siSetupAmount: "N",
            siAmount: "",
            siStartDate: dateToday,
            siFrequencyType: "",
            siFrequency: "",
            siBillCycle: ""
        )
        paymentController?.delegate = self;
        self.present(paymentController!, animated: true, completion: nil);
    }
    
    func getResponse(_ responseDict_: NSMutableDictionary!)
    {
        self.blankView.isHidden = false
        print(responseDict_)
        let orderNum = "\(responseDict_["order_id"] ?? "")"
        let orderStatus = "\(responseDict_["order_status"] ?? "")"
        print(orderStatus)
      //  let orderTrackId = "\(responseDict_["tracking_id"] ?? "")"
        //  if orderStatus == "Success" {
        let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "OrderPlacedViewController") as! OrderPlacedViewController
        vc.orderId = orderNum
        vc.orderType = self.paymentMode
        vc.orderStatus = orderStatus
        vc.addrDict = self.deafaultAddressDict
        vc.subTotal =  self.lblSubTotal.text!
        vc.discount = self.lblDiscount.text!
        vc.deliveryCharge =  self.lblDeliveryCharges.text!
        vc.total = self.lblTotalAmount.text!
        vc.succFailRes = responseDict_
        //              self.PurchaseEvent(order_id : self.customerOrderId)
        //            let dictParam :[String:Any] = ["Content_ID":"\(self.customerOrderId)","Currency": "AED", "ValueToSum":"\(self.lblTotalAmount.text!)"]
        //            print(dictParam)
        //            self.PurchaseEvents(dictParam: dictParam)
        self.navigationController?.pushViewController(vc, animated: true)
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
                
                self.rsaKeyURLTF = baseUrl + "get-rsa-demo/?order_id=\(self.customerOrderId)" //Demo
                // self.rsaKeyURLTF = baseUrl + "get-rsa-demo" //Demo
               // self.rsaKeyURLTF = "https://www.gogrocery.ae/api/front/v1/get-rsa/" //Live
                self.MakeDemoPayment()
            }
        }
    }
    
    func getAddressFromApiCall(){
        print(deafaultAddressDict)
        self.lblName.text = deafaultAddressDict["delivery_name"]?.string ?? ""
        self.lblApartment.text = deafaultAddressDict["delivery_street_address"]?.string ?? ""
       // self.lblCountry.text = deafaultAddressDict["delivery_state_name"].stringValue + " " + deafaultAddressDict["delivery_country_name"]!.stringValue
         self.lblCountry.text =  deafaultAddressDict["delivery_country_name"]?.string ?? ""
        self.lblMobile.text = deafaultAddressDict["delivery_phone"]?.string ?? ""
        self.addressId = deafaultAddressDict["id"]?.int ?? 0
        
        self.billingNameTF = deafaultAddressDict["billing_name"]?.string ?? ""
        self.billingAddressTF = deafaultAddressDict["billing_street_address"]?.string ?? ""
        self.billingCityTF = deafaultAddressDict["billing_city"]?.string ?? "Basara"
        self.billingStateTF = deafaultAddressDict["billing_state_name"]?.string ?? ""
        self.billingCountryTF = deafaultAddressDict["billing_country_name"]?.string ?? ""
        self.billingTelTF = deafaultAddressDict["billing_phone"]?.string ?? ""
        self.billingEmailTF = deafaultAddressDict["billing_email_address"]?.string ?? ""
        
        self.shippingNameTF = deafaultAddressDict["delivery_name"]?.string ?? ""
        self.shippingAddressTF = deafaultAddressDict["delivery_street_address"]?.string ?? ""
        self.shippingCityTF = deafaultAddressDict["delivery_country_name"]?.string ?? ""
        self.shippingStateTF = deafaultAddressDict["delivery_country_name"]?.string ?? ""
        self.shippingCountry = deafaultAddressDict["delivery_country_name"]?.string ?? ""
        self.shippingTelTF = deafaultAddressDict["delivery_phone"]?.string ?? ""
    }
    
    //MARK:- Events
    
//    func InitiateCheckout(dictParam : [String:Any]) {
//        Analytics.logEvent("initiate_checkout", parameters:  dictParam)
//    }
    
    //    MARK:- Alert
    func showAlert32(message: String)
    {
        let alert = UIAlertController(title: "Alert", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
            self.navigationController?.popViewController(animated: true)
        }))
        self.present(alert, animated: true, completion: nil)
    }
}
extension DeliveryDetailsViewController : UITableViewDataSource , UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.paymentMethodArr.count
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        if indexPath.row == self.paymentSelectIndex {
            return 80
        }
        else {
            return 40
        }
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = Bundle.main.loadNibNamed("PaymentMethodTableViewCell", owner: self, options: nil)?.first as! PaymentMethodTableViewCell
        let dict = self.paymentMethodArr[indexPath.row].dictionaryValue
        let dict1 = dict["engageboost_paymentgateway_method_id"]?.dictionaryValue
        cell.lblPaymentType.text = dict1?["name"]?.string ?? ""
        if self.paymentIdArr.contains(dict1?["id"]?.int ?? 0) {
            cell.imgImage.image = UIImage(named: "radio_select")
        }
        else {
            cell.imgImage.image = UIImage(named: "radio_unselect")
        }
        if paymentMethodName == "Credit / Debit Card(Online Payment)" {
            if indexPath.row == self.paymentSelectIndex {
               // self.paymentSelectIndex = indexPath.row
                self.viewPaymentHeight.constant = CGFloat(40*self.paymentMethodArr.count) + 41
                cell.lblTerms.text = "* For verification, an amount of AED 1 will be charged. The amount will be reversed automatically."
                cell.lblTerms.textColor = UIColor.red
                  cell.lblTerms.alpha = 1
            }
            else {
                cell.lblTerms.alpha = 0
                cell.lblTerms.text = ""
                cell.lblTerms.textColor = UIColor.white
               // self.paymentSelectIndex = 9999
              //  self.viewPaymentHeight.constant = CGFloat(40*self.paymentMethodArr.count) + 1
                 cell.lblTerms.isHidden = true
            }

        }
        else {
            cell.lblTerms.alpha = 0
            cell.lblTerms.text = ""
            cell.lblTerms.textColor = UIColor.white
          //  self.paymentSelectIndex = 9999
           // self.viewPaymentHeight.constant = CGFloat(40*self.paymentMethodArr.count) + 1
             cell.lblTerms.isHidden = true
        }
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
       //   let cell = Bundle.main.loadNibNamed("PaymentMethodTableViewCell", owner: self, options: nil)?.first as! PaymentMethodTableViewCell
        let dict = self.paymentMethodArr[indexPath.row].dictionaryValue
        let dict1 = dict["engageboost_paymentgateway_method_id"]?.dictionaryValue
        self.paymentId = dict1?["id"]?.int ?? 0
        self.paymentgateway_type_id = dict1?["paymentgateway_type_id"]?.int ?? 0
        self.paymentIdArr.removeAll()
        self.paymentIdArr.append(self.paymentId)
        self.paymentMode = dict1?["name"]?.string ?? ""
        self.paymentMethodName = dict1?["name"]?.string ?? ""
        if paymentMethodName == "Credit / Debit Card(Online Payment)" {
            self.paymentSelectIndex = indexPath.row
             self.viewPaymentHeight.constant = CGFloat(40*self.paymentMethodArr.count) + 41
        }
        else {
            self.paymentSelectIndex = 9999
            self.viewPaymentHeight.constant = CGFloat(40*self.paymentMethodArr.count) + 1
        }
        self.tableView.reloadData()
        print("Payment ID ------------->>>>>>>>>>>>> \(self.paymentId)")
        print("Payment Gateway ID ------------->>>>>>>>>>>>> \(self.paymentgateway_type_id)")
    }
}
