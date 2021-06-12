
import UIKit
import SwiftyJSON
import NVActivityIndicatorView
class PresentOrdersViewController: UIViewController {

    @IBOutlet weak var presentOrderTabel: UITableView!
    var orderNumArr = [String]()
    var dateArr = [String]()
    var amtArr = [String]()
    var paymentStatusArr = [String]()
    var orderStatusArr = [String]()
    var idArr = [String]()
    var orderArr = [JSON]()
    var paymentModeArr = [String]()
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
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
        self.presentOrderTabel.reloadData()
        getOrderDetails()
    }
    
    func getOrderDetails() {
        let auth = UserDefaults.standard.value(forKey: "token") as! String
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        let headers:[String : Any] = ["Authorization": "Token \(auth)","WAREHOUSE":"\(wareHouseId)","WID":"1"]
        
        let activityData = ActivityData()
        NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
        DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
        
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "order-history/?req_type=present", vc: self, header: headers) { (response) in
            print(response)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            if response["status"].stringValue == "200" {
                self.orderArr = response["data"].arrayValue
                let data = response["data"].arrayValue
                print("data... \(data)")
                for order in data {
                    self.orderNumArr.append(order["custom_order_id"].stringValue)
                    self.dateArr.append(order["created"].stringValue)
                    let dd = String(format: "%.2f", order["gross_amount"].doubleValue)
                    let amt = "\(dd)"
                    let curCode = order["currency_code"].stringValue
                    self.amtArr.append("\(curCode) \(amt)")
                    self.paymentStatusArr.append(order["str_payment_status"].stringValue)
                    self.orderStatusArr.append(order["str_order_status"].stringValue)
                    self.idArr.append("\(order["id"].intValue)")
                    self.paymentModeArr.append(order["payment_method_name"].stringValue)
                }
                self.presentOrderTabel.delegate = self
                self.presentOrderTabel.dataSource = self
                self.presentOrderTabel.reloadData()
                print(self.orderNumArr)
                print(self.dateArr)
            }
            else {
                 createalert(title: "Alert", message: response["message"].stringValue, vc: self)
            }
        }
    }
    
}

extension PresentOrdersViewController : UITableViewDataSource , UITableViewDelegate {
    
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
        let cell = presentOrderTabel.dequeueReusableCell(withIdentifier: "PresentOrderTableViewCell") as! PresentOrderTableViewCell
        cell.selectionStyle = .none
        cell.orderNoLabel.text = "Order No: \(orderNumArr[indexPath.row])"
        let dateFormatter = DateFormatter()
        // TODO: implement dateFromSwapiString
        let createdDate = dateFormatter.date(fromSwapiString: dateArr[indexPath.row])
        print(createdDate)
        //let dayTimePeriodFormatter = DateFormatter()
        dateFormatter.dateFormat = "MMM dd YYYY hh:mm a"

        let dateString = dateFormatter.string(from: createdDate!)
        cell.orederDateLabel.text = "\(dateString)"
        cell.priceLabel.text = amtArr[indexPath.row]
        
        let stringValue = "Payment status: \(paymentStatusArr[indexPath.row])"
        let attributedString: NSMutableAttributedString = NSMutableAttributedString(string: stringValue)
        attributedString.setColorForText(textForAttribute: "Payment status: ", withColor: UIColor.black)
        if paymentStatusArr[indexPath.row] == "Unpaid" {
            attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: #colorLiteral(red: 1, green: 0.1491314173, blue: 0, alpha: 1))
        } else if paymentStatusArr[indexPath.row] == "Successful" {
            attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: #colorLiteral(red: 0.266835967, green: 0.5173968299, blue: 0.8054970855, alpha: 1))
        } else {
            attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: #colorLiteral(red: 0.3411764801, green: 0.6235294342, blue: 0.1686274558, alpha: 1))
        }
        //attributedString.setColorForText(textForAttribute: "\(paymentStatusArr[indexPath.row])", withColor: UIColor.green)
        cell.paymentStatusLabel.attributedText = attributedString
        cell.orderStatusLabel.text = "Order Status: \(orderStatusArr[indexPath.row])"
        cell.paymentModeLabel.text = "Payment Mode: \(self.paymentModeArr[indexPath.row])"
        cell.backgroundColor = .clear
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
        let orderDict = self.orderArr[indexPath.row].dictionaryValue
        print(orderDict)

        vc.orderId = idArr[indexPath.row]
        let customorderId = "\(orderDict["custom_order_id"]!.intValue)"
        UserDefaults.standard.set(customorderId, forKey: "custom_order_id")
        UserDefaults.standard.set(idArr[indexPath.row], forKey: "order_id")
        UserDefaults.standard.synchronize()
            let dateFormatter = DateFormatter()
            // TODO: implement dateFromSwapiString
            let createdDate = dateFormatter.date(fromSwapiString: dateArr[indexPath.row])
            
            //let dayTimePeriodFormatter = DateFormatter()
            dateFormatter.dateFormat = "dd MMM YYYY hh:mm a"
            let dateString = dateFormatter.string(from: createdDate!)
           // vc.orderDate = dateString
            vc.isFromPastOrder = false
            self.navigationController?.pushViewController(vc, animated: true)
    }
    
    
    
}

extension DateFormatter {
  func date(fromSwapiString dateString: String) -> Date? {
    // SWAPI dates look like: "2014-12-10T16:44:31.486000Z"  "yyyy-MM-dd'T'HH:mm:ss.SZ"
    self.dateFormat = "yyyy-MM-dd'T'HH:mm:ss.SZ"
    self.timeZone = TimeZone(abbreviation: "UTC")
    self.locale = Locale(identifier: "en_US_POSIX")
    return self.date(from: dateString)
  }
}

extension NSMutableAttributedString {

    func setColorForText(textForAttribute: String, withColor color: UIColor) {
        let range: NSRange = self.mutableString.range(of: textForAttribute, options: .caseInsensitive)

        // Swift 4.2 and above
        self.addAttribute(NSAttributedString.Key.foregroundColor, value: color, range: range)

        // Swift 4.1 and below
        //self.addAttribute(NSAttributedStringKey.foregroundColor, value: color, range: range)
    }

}
