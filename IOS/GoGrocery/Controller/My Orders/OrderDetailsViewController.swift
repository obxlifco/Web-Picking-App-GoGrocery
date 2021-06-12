//
//  OrderDetailsViewController.swift
//  GoGrocery
//
//  Created by Nav121 on 06/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import Alamofire
//import SVProgressHUD
import SwiftyJSON

class OrderDetailsViewController: UIViewController  {
    @IBOutlet weak var btnCartCount: UIButton!
    @IBOutlet weak var btnCart: UIButton!
    @IBOutlet weak var orderDetailsTable: UITableView!
    @IBOutlet weak var cancelButton: UIButton!
    @IBOutlet weak var cancelView: UIView!
    @IBOutlet weak var btnPayNow: UIButton!
    @IBOutlet weak var dropDownReasonButton: UIButton!
    @IBOutlet weak var cancelpopupView: UIView!
    @IBOutlet weak var cancelReasonView: UIView!
    @IBOutlet weak var cancelreasonTable: UITableView!
    var cancelReason = ["Wrong product selected","Wrong price","Order by mistake","Other"]
    var orderId = ""
    var orderDate = ""
    var infoArr = ["":""]
    var productNameArr = [String]()
    var productPriceArr = [String]()
    var productImageArr = [String]()
    var isReasonSelected = false
    var reasonNo = 99
    var isFromPastOrder = false
    var orderDetailsDict = [String:JSON]()
    var orderProducts = [JSON]()
    var cartArray = [JSON]()
    var badgeCount = Int()
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var paymentTokenInReset: String = ""
    var pageFrom:String = ""
    var customMsg:String = ""
    var isFromPush:String = ""
    //  var paymentController = CCAvenuePaymentController()
    
    @IBOutlet weak var mainCancelViewHeight: NSLayoutConstraint!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        orderDetailsTable.allowsSelection = false
        let tap = UITapGestureRecognizer(target: self, action: #selector(self.handleTap(_:)))
        cancelView.addGestureRecognizer(tap)
        let tap1 = UITapGestureRecognizer(target: self, action: #selector(self.handlePopupViewTap(_:)))
        cancelpopupView.addGestureRecognizer(tap1)
        //let tap2 = UITapGestureRecognizer(target: self, action: #selector(self.handleCancelViewTap(_:)))
        //cancelReasonView.addGestureRecognizer(tap2)
        
        arrangeView()
        getOrderDetails()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        cancelView.alpha = 0
        cancelReasonView.alpha = 0
        navigationController?.setNavigationBarHidden(true, animated: true)
        //ApiCallToViewCart()
        ApiCallToGetCartCount()
    }
    
    @objc func handleTap(_ sender: UITapGestureRecognizer? = nil) {
        print("handletap")
        UIView.animate(withDuration: 0.3, delay: 0.0, options: [], animations: {
            self.cancelView.alpha = 0
            self.cancelReasonView.alpha = 0
            
        })
    }
    
    @objc func handlePopupViewTap(_ sender: UITapGestureRecognizer? = nil) {
        print("handlepopuptap")
        UIView.animate(withDuration: 0.3, delay: 0.0, options: [], animations: {
            self.cancelReasonView.alpha = 0
            
        })
    }
    
    @objc func handleCancelViewTap(_ sender: UITapGestureRecognizer? = nil) {
        print("handlepopuptap")
        
    }
    
    func arrangeView() {
        cancelButton.layer.cornerRadius = 6
        cancelButton.clipsToBounds = true
        cancelButton.layer.borderWidth = 1
        cancelButton.layer.borderColor = UIColor.red.cgColor
        
        dropDownReasonButton.layer.cornerRadius = 6
        dropDownReasonButton.clipsToBounds = true
        dropDownReasonButton.layer.borderWidth = 1
        dropDownReasonButton.layer.borderColor = UIColor.black.cgColor
        if isFromPastOrder == true {
            self.mainCancelViewHeight.constant = 0
        }
    }
    
    @IBAction func cartButtonTapped(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "CartViewController") as! CartViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func backButtonTapped(_ sender: Any) {
        if isFromPush == "Push" {
            let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
            self.navigationController?.pushViewController(vc, animated: true)
        }
        else {
            self.navigationController?.popViewController(animated: true)
        }
       
    }
    
    @IBAction func cancelButtonTapped(_ sender: Any) {
        isReasonSelected = false
        dropDownReasonButton.setTitle("Select reason for cancellation*", for: .normal)
        cancelReasonView.alpha = 0
        cancelView.alpha = 1
        cancelpopupView.alpha = 0
        let screenSize = UIScreen.main.bounds.size
        let originalY = cancelpopupView.frame.origin.y
        cancelpopupView.frame.origin.y = screenSize.height
        UIView.animate(withDuration: 0.4, delay: 0.0, options: [], animations: {
            self.cancelpopupView.alpha = 1
            self.cancelpopupView.frame.origin.y = originalY
            
        })
    }
    @IBAction func cancelReasonPopupButtonTapped(_ sender: Any) {
        UIView.animate(withDuration: 0.3, delay: 0.0, options: [], animations: {
            self.cancelView.alpha = 0
            self.cancelReasonView.alpha = 0
        })
    }
    @IBAction func submitButtonTapped(_ sender: Any) {
        if isReasonSelected == true {
            let id = Int(self.orderId)
            var params = [String:Any]()
            params["return_note"] = cancelReason[reasonNo]
            params["order_id"] = id
            
           // SVProgressHUD.show()
            postMethodQueryWithAuthorization(apiName: "cancel-order/\(self.orderId)/", params: params, vc: self) { (response) in
                print(response)
                if response["status"].stringValue == "200" {
                   // SVProgressHUD.dismiss()
                    createalert(title: "Message", message: "Order cancelled successfully", vc: self)
                    //  DispatchQueue.main.async {
                    self.cancelView.alpha = 0
                    self.cancelButton.alpha = 0
                    self.mainCancelViewHeight.constant = 0
                    // }
                    
                } else {
                    //                    let msg = response["message"].stringValue
                  //  SVProgressHUD.dismiss()
                    createalert(title: "Alert", message: response["message"].stringValue, vc: self)
                }
            }
        } else {
            createalert(title: "Alert", message: "Please select a reason", vc: self)
        }
    }
    @IBAction func dropDownReasonButtonTapped(_ sender: Any) {
        UIView.animate(withDuration: 0.5, delay: 0.0, options: [], animations: {
            self.cancelReasonView.alpha = 1
            
        })
    }
    
    @IBAction func cancelPopupBackTapped(_ sender: Any) {
        UIView.animate(withDuration: 0.3, delay: 0.0, options: [], animations: {
            self.cancelView.alpha = 0
            self.cancelReasonView.alpha = 0
        })
    }
  /*
    @IBAction func btnPayNowAction(_ sender: Any) {
        if pageFrom == "deepLink" {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                let vc = self.storyboard!.instantiateViewController(withIdentifier: "NewPaymentViewController") as! NewPaymentViewController
                let backButton = UIBarButtonItem()
                backButton.title = ""
                navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
                self.navigationController?.pushViewController(vc, animated: true)
            }
            else {
                let storyboard:UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "LoginViewController") as! LoginViewController
//                let backButton = UIBarButtonItem()
//                backButton.title = ""
//                navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
                self.navigationController?.pushViewController(vc, animated: true)
            }

        }
        else {
            let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "NewPaymentViewController") as! NewPaymentViewController
            self.navigationController?.pushViewController(vc, animated: true)
        }
        
    }
 */
    func getOrderDetails() {
            let auth = UserDefaults.standard.value(forKey: "token") as! String
            let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
            let headers:[String : Any] = ["Authorization": "Token \(auth)","WAREHOUSE":"\(wareHouseId)","WID":"1" , "Content-Type": "application/json"]
        //    SVProgressHUD.show()
            getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "order-details/\(self.orderId)/", vc: self, header: headers) { (response) in
                print(response)
             //   SVProgressHUD.dismiss()
                if response["status"].stringValue == "200" {
                    let data = response["data"].dictionaryValue
                    self.orderDetailsDict = response["data"].dictionaryValue
                    self.customMsg = self.orderDetailsDict["custom_msg"]?.string ?? ""
                    print("data... \(data)")
                    self.infoArr["name"] = data["billing_name"]?.string ?? ""
                    self.infoArr["address"] = data["billing_street_address"]?.string ?? ""
                    self.infoArr["country"] = data["billing_country_name"]?.string ?? ""
                    self.infoArr["mobile"] = data["billing_phone"]?.string ?? ""
                    let sb = String(format: "%.2f", data["net_amount"]?.double ?? 0.00)
                    self.infoArr["subTotal"] = "\(sb)"
                    
                    let orderDate  = data["created"]?.stringValue
                    let dateFormatter = DateFormatter()
                      // TODO: implement dateFromSwapiString
                    let createdDate = dateFormatter.date(fromSwapiString: orderDate!)
                      //let dayTimePeriodFormatter = DateFormatter()
                      dateFormatter.dateFormat = "dd MMM YYYY hh:mm a"
                      let dateString = dateFormatter.string(from: createdDate!)
                        self.orderDate = dateString
                     // self.dateArr.append(order["created"].stringValue)

                    let gda = data["gross_discount_amount"]?.string ?? "0"
                    let myDouble = gda.toDouble()
                    let gdas = String(format: "%.2f", myDouble ?? 0.00)
                     self.infoArr["discount"] = gdas
                    
                   // self.infoArr["delivery"] = data["shipping_cost"]?.stringValue
                    let  sc = data["shipping_cost"]?.double ?? 0.00
                   // let md = sc.toDouble()
                    let scc = String(format: "%.2f", sc ?? 0.00)
                    self.infoArr["delivery"] = scc
                    
                    
                    let ga = String(format: "%.2f", data["gross_amount"]?.double ?? 0.00)
                    self.infoArr["total"] = "\(ga)"
                    
                    self.infoArr["orderNumber"] = "\(data["custom_order_id"]?.string ?? "")"
                    let productAr = data["order_products"]?.arrayValue
                    self.orderProducts = data["order_products"]!.arrayValue
                    if let productArr = productAr {
                        for product in productArr {
                            let productDict = product["product"].dictionaryValue
                            self.productNameArr.append(productDict["name"]!.string ?? "")
                            let price = String(format: "%.2f", product["new_default_price"].double ?? 0.00)
                            self.productPriceArr.append("\(price)")
                            let productImage = productDict["product_image"]?.dictionaryValue
                            if let imageDict = productImage {
                                self.productImageArr.append(imageDict["img"]!.string ?? "")
                            } else {
                                self.productImageArr.append("")
                            }
                        }
                    }
                    let shipmentStatus = self.orderDetailsDict["shipment_status"]!.string ?? ""
                    print(shipmentStatus)
                    if shipmentStatus == "Invoicing" {
//                        self.btnPayNow.isHidden = false
//                        self.btnPayNow.layer.cornerRadius = 5
//                        self.btnPayNow.addShadow2()
                    }
                    else  {
                      //  self.btnPayNow.isHidden = true
                    }
                    
                    if shipmentStatus == "Invoicing" {
                        self.cancelButton.isHidden = false
                    }
                    else if shipmentStatus == "Pending" {
                         self.cancelButton.isHidden = false
                    }
                    else if shipmentStatus == "Picking" {
                         self.cancelButton.isHidden = false
                       }
                    else if shipmentStatus == "" {
                         self.cancelButton.isHidden = false
                       }
                    else {
                        self.cancelButton.isHidden = true
                    }
                    self.orderDetailsTable.reloadData()
                    print("info")
                    print(self.productNameArr)
                    print(self.productPriceArr)
                    print(self.productImageArr)
                }
                else {
//                    createalert(title: "Alert", message: "Something went wrong , please try after sometime", vc: self)
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
                    //                    self.collectionView.reloadData()
                }
                else {
                    //                    self.cartArra
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
            getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "view-cart/", vc: self, header: headers) { (response: JSON) in
                print(response)
                if response["status"].intValue == 200 {
                    self.cartArray = response["data"].arrayValue
                    self.badgeCount = response["cart_count_itemwise"].intValue
                    self.btnCartCount.setTitle("\(self.badgeCount)", for: .normal)
                    self.btnCartCount.isHidden = false
                    self.btnCart.setImage(UIImage(named: "cart"), for: .normal)
                    //                       self.collectionView.reloadData()
                    //                    self.viewDidLayoutSubviews()
                    //  self.addRightBarButtonItems(badge: self.cartArray.count)
                }
                else {
                    //                    self.collectionView.reloadData()
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
    
}

extension OrderDetailsViewController : UITableViewDataSource , UITableViewDelegate {
    
    func numberOfSections(in tableView: UITableView) -> Int {
        if tableView == orderDetailsTable {
            return 2
        } else {
            return 1
        }
        
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if tableView == orderDetailsTable {
            if section == 0 {
                return 1
            } else {
                return productNameArr.count
            }
        } else {
            return cancelReason.count
        }
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if tableView == orderDetailsTable {
            if indexPath.section == 0 {
                let cell = orderDetailsTable.dequeueReusableCell(withIdentifier: "OrderDetailsTableViewCell") as! OrderDetailsTableViewCell
                cell.backgroundColor = #colorLiteral(red: 0.978994443, green: 0.978994443, blue: 0.978994443, alpha: 0.6675286092)
                cell.orderNoLabel.text = "Order No: \(self.infoArr["orderNumber"] ?? "0")"
                cell.orderDatelabel.text = self.orderDate
                cell.shippingNameLabel.text = self.infoArr["name"]
                cell.shippingAddress1Label.text = self.infoArr["address"]
                cell.shippingAddress2Label.text = self.infoArr["country"]
                cell.shippingMobileNoLabel.text = self.infoArr["mobile"]
                cell.subtotalLabel.text = "AED \(self.infoArr["subTotal"] ?? "0")"
                cell.discountlabel.text = "AED \(self.infoArr["discount"] ?? "0")"
                cell.deliverylabel.text = "AED \(self.infoArr["delivery"] ?? "0")"
                cell.totalAmtLabel.text = "AED \(self.infoArr["total"] ?? "0")"
               
                if self.customMsg.isEmpty == false {
                  cell.lblNoteDes.text = self.customMsg
                    cell.heightCardView.constant = 90
                    cell.heightLblNote.constant = 30
                    cell.heightLblNoteDes.constant = 30
                    cell.lblNote.isHidden = false
                    cell.lblNoteDes.isHidden = false
                }
                else {
                    cell.heightCardView.constant = 60
                    cell.heightLblNote.constant = 0
                    cell.heightLblNoteDes.constant = 0
                    cell.lblNote.isHidden = true
                    cell.lblNoteDes.isHidden = true
                }
                return cell
            }
            else {
                let cell = orderDetailsTable.dequeueReusableCell(withIdentifier: "OrderItemTableViewCell") as! OrderItemTableViewCell
                //cell.backgroundColor = #colorLiteral(red: 0.8684050648, green: 0.8684050648, blue: 0.8684050648, alpha: 1)
                let orderProductDict = self.orderProducts[indexPath.row].dictionaryValue
                
                cell.itemNameLabel.text = self.productNameArr[indexPath.row]
                
                cell.itemAmountLabel.text = "AED \(self.productPriceArr[indexPath.row])"
              //  let strikedAmt =  "\(self.orderDetailsDict["order_products"]![indexPath.row]["cost_price"].doubleValue)"
                
                let na = String(format: "%.2f", self.orderDetailsDict["order_products"]![indexPath.row]["cost_price"].double ?? 0.00)
               // self.infoArr["subTotal"] = "\(na)"
                let strikedAmt1 =  "AED \(na)"
                print(self.productPriceArr[indexPath.row])
                let strikedAmtInt:Double = Double(na) ?? 0.0
                let dp:Double = Double(self.orderDetailsDict["order_products"]![indexPath.row]["new_default_price_unit"].double ?? 0.00)
//                print(strikedAmtInt)
//                print(dp)
//                print(self.productPriceArr[indexPath.row])
                if strikedAmtInt > dp {
                    let attributeString: NSMutableAttributedString =  NSMutableAttributedString(string: strikedAmt1)
                    attributeString.addAttribute(NSAttributedString.Key.strikethroughStyle, value: 2, range: NSMakeRange(0, attributeString.length))
                    cell.lblStrike.attributedText = attributeString
                    cell.lblStrike.isHidden = false
                } else {
                    cell.lblStrike.isHidden = true
                }
                   if (self.productImageArr[indexPath.row] as? String)!.isEmpty == false {
             //   if let url = self.productImageArr[indexPath.row] as? String {
                    let url = self.productImageArr[indexPath.row]
                    let urlString = "https://d1fw2ui0wj5vn1.cloudfront.net/Lifco/lifco/product/200x200/\(url)"
                    let imageUrl = URL(string: urlString)!
                    cell.itemImageView.sd_setImage(with: imageUrl, placeholderImage: nil)
                }
                else {
                    cell.itemImageView.image = UIImage(named:"no_image")
                }

                
                let productDict = orderProductDict["product"]?.dictionaryValue
                let unitWeight = productDict!["weight"]!.string ?? ""
                
                if let productUnitDict = productDict!["uom"]!.dictionary {
                    //                    let productUnitDict = productUnitDict
                    let productUnit = productUnitDict["uom_name"]!.string ?? ""
                    let productQuantity = orderProductDict["quantity"]!.int ?? 0
                    cell.lblUnitItem.text = "Product Unit : \(unitWeight) \(productUnit) * \(productQuantity)"
                    
                }
                else {
                    
                }
                let unitPrice = orderProductDict["new_default_price_unit"]!.double ?? 0.00
                let price = String(format: "%.2f", unitPrice)
                cell.lblUnitPrice.text = "Unit Price : AED \(price)"
                
                if orderProductDict["grn_quantity"]?.intValue == 0 &&  orderProductDict["quantity"]?.int ?? 0 == 0 {
                    cell.lblStock.isHidden = false
                    cell.lblOutOfStockHeight.constant = 20
                }
                else {
                    cell.lblStock.isHidden = true
                    cell.lblOutOfStockHeight.constant = 0
                }
                return cell
            }
            
        }
        else {
            let cell = cancelreasonTable.dequeueReusableCell(withIdentifier: "OrederCancelReasonTableViewCell") as! OrederCancelReasonTableViewCell
            cell.reasonLabel.text = cancelReason[indexPath.row]
            return cell
        }
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        if tableView == orderDetailsTable {
            if indexPath.section == 0 {
                
                return 450
            } else {
                return 120
            }
        } else {
            return 40
        }
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if tableView == cancelreasonTable {
            let reason = cancelReason[indexPath.row]
            dropDownReasonButton.setTitle(reason, for: .normal)
            isReasonSelected = true
            reasonNo = indexPath.row
            self.cancelReasonView.alpha = 0
            print(indexPath.row)
        } else {
            print(indexPath)
        }
    }
    
    
}
extension String {
    func toDouble() -> Double? {
        return NumberFormatter().number(from: self)?.doubleValue
    }
}
