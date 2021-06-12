//
//  WalletViewController.swift
//  GoGrocery
//
//  Created by Nav63 on 11/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class WalletViewController: UIViewController ,UITableViewDelegate , UITableViewDataSource{

    @IBOutlet weak var tableView: UITableView!
    var walletArray = [JSON]()
    override func viewDidLoad() {
        super.viewDidLoad()

        self.title = "My Wallet"
        ApiCallToGetWalletData()
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = false
    }
//    MARK:- TableView Delegate and Data Source
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 130
    }
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.walletArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "WalletTableViewCell", for: indexPath) as! WalletTableViewCell
        let walletDict = walletArray[indexPath.row].dictionaryValue
        let dateZone = walletDict["valid_form"]?.stringValue
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss.SSSSZ"
        let date = dateFormatter.date(from: dateZone!)

        dateFormatter.dateFormat = "MM/dd/yyyy"
        let goodDate = dateFormatter.string(from: date!)
        print(dateFormatter.string(from: date!))
        cell.lblDate.text = "\(goodDate)"
        
        cell.lblEarnedPoints.text = "\(walletDict["received_points"]!.doubleValue)"
        cell.lblUsedPoints.text = "\(walletDict["burnt_points"]!.doubleValue)"
        cell.lblRemainingPoints.text = "\(walletDict["remaining_balance"]!.doubleValue)"
        return cell
    }
    
    func ApiCallToGetWalletData() {
        let auth = UserDefaults.standard.value(forKey: "token") as! String
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
          let headers:[String : Any] = ["Authorization": "Token \(auth)","WAREHOUSE":"\(wareHouseId)","WID":"1"]
        getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: "points-log/", vc: self, header: headers) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                if response["data"].arrayValue.count != 0 {
                    self.walletArray = response["data"].arrayValue
                    self.tableView.dataSource = self
                    self.tableView.delegate = self
                    self.tableView.reloadData()
                }
            }
            else {
                
            }
        }
    }
    
}

