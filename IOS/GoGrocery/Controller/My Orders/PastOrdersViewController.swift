//
//  PastOrdersViewController.swift
//  GoGrocery
//
//  Created by Nav121 on 05/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class PastOrdersViewController: UIViewController {

    @IBOutlet weak var pastOrderTable: UITableView!
    var orderNumArr = [String]()
    var dateArr = [String]()
    var amtArr = [String]()
    var paymentStatusArr = [String]()
    var orderStatusArr = [String]()
    var idArr = [String]()
    var paymentModeArr = [String]()
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        //getOrderDetails()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.paymentModeArr.removeAll()
        orderNumArr.removeAll()
        dateArr.removeAll()
        amtArr.removeAll()
        paymentStatusArr.removeAll()
        orderStatusArr.removeAll()
        idArr.removeAll()
        self.pastOrderTable.reloadData()
        getOrderDetails()
    }
    
    func getOrderDetails() {
        let auth = UserDefaults.standard.value(forKey: "token") as! String
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        let headers:[String : Any] = ["Authorization": "Token \(auth)","WAREHOUSE":"\(wareHouseId)","WID":"1"]
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "order-history/?req_type=past", vc: self, header: headers) { (response) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].arrayValue
                print("data... \(data)")
                for order in data {
                    self.orderNumArr.append(order["custom_order_id"].stringValue)
                    self.dateArr.append(order["created"].stringValue)
                    let dd = String(format: "%.2f", order["gross_amount"].doubleValue)
                  //  let amt = "\(order["gross_amount"].doubleValue)"
                    let curCode = order["currency_code"].stringValue
                    self.amtArr.append("\(curCode) \(dd)")
                    self.paymentStatusArr.append(order["str_payment_status"].stringValue)
                    self.orderStatusArr.append(order["str_order_status"].stringValue)
                    self.idArr.append("\(order["id"].intValue)")
                    self.paymentModeArr.append(order["payment_method_name"].stringValue)
                }
                self.pastOrderTable.delegate = self
                self.pastOrderTable.dataSource = self
                self.pastOrderTable.reloadData()
                print(self.orderNumArr)
                print(self.dateArr)
            }
            else {
                createalert(title: "Alert", message: response["message"].stringValue, vc: self)
            }
        }
    }
}
extension PastOrdersViewController : UITableViewDataSource , UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if self.orderNumArr.count != 0 {
            return self.orderNumArr.count
        }
        else {
            return 0
        }
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 160.00
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = pastOrderTable.dequeueReusableCell(withIdentifier: "PresentOrderTableViewCell") as! PresentOrderTableViewCell
        cell.selectionStyle = .none
        cell.orderNoLabel.text = "Order No: \(orderNumArr[indexPath.row])"
        let dateFormatter = DateFormatter()
        // TODO: implement dateFromSwapiString
        let createdDate = dateFormatter.date(fromSwapiString: dateArr[indexPath.row])
        print(createdDate)
        //let dayTimePeriodFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd MMM YYYY hh:mm a"

        let dateString = dateFormatter.string(from: createdDate!)
        cell.orederDateLabel.text = "\(dateString)"
        cell.priceLabel.text = amtArr[indexPath.row]
        
        let stringValue = "Payment status: \(paymentStatusArr[indexPath.row])"
        let attributedString: NSMutableAttributedString = NSMutableAttributedString(string: stringValue)
        attributedString.setColorForText(textForAttribute: "Payment status: ", withColor: UIColor.black)
        if paymentStatusArr[indexPath.row] == "Unpaid" {
            attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: #colorLiteral(red: 0.3079027053, green: 0.7381598122, blue: 0.2436443673, alpha: 1))
        } else if paymentStatusArr[indexPath.row] == "Successful" {
            attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: #colorLiteral(red: 0.266835967, green: 0.5173968299, blue: 0.8054970855, alpha: 1))
        } else {
            attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: #colorLiteral(red: 0.8182682966, green: 0.168703415, blue: 0.05925517245, alpha: 1))
        }
        //attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: UIColor.green)
        cell.paymentStatusLabel.attributedText = attributedString
        //cell.orderStatusLabel.textColor = #colorLiteral(red: 0.9201546308, green: 0.1863558946, blue: 0.1600643869, alpha: 1)
        let orderString = "Order Status: \(orderStatusArr[indexPath.row])"
        let attributedString1: NSMutableAttributedString = NSMutableAttributedString(string: orderString)
        attributedString1.setColorForText(textForAttribute: "Order Status: ", withColor: UIColor.black)
        attributedString1.setColorForText(textForAttribute: "\(orderStatusArr[indexPath.row])", withColor: #colorLiteral(red: 0.8182682966, green: 0.168703415, blue: 0.05925517245, alpha: 1))
        
        cell.orderStatusLabel.attributedText = attributedString1
        cell.backgroundColor = .clear
        cell.paymentModeLabel.text = "Payment Mode: \(self.paymentModeArr[indexPath.row])"
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
            vc.orderId = idArr[indexPath.row]
            let dateFormatter = DateFormatter()
            // TODO: implement dateFromSwapiString
            let createdDate = dateFormatter.date(fromSwapiString: dateArr[indexPath.row])
            
            //let dayTimePeriodFormatter = DateFormatter()
            dateFormatter.dateFormat = "dd MMM YYYY hh:mm a"
            let dateString = dateFormatter.string(from: createdDate!)
            vc.orderDate = dateString
            vc.isFromPastOrder = true
            self.navigationController?.pushViewController(vc, animated: true)
    }
    
    
}
