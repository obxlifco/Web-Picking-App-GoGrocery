//
//  SavedAdressListViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 29/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class SavedAdressListViewController: UIViewController {
    
    @IBOutlet weak var lblTitle: UILabel!
    @IBOutlet weak var btnDeliverHeight: NSLayoutConstraint!
    @IBOutlet weak var viewAddressCount: UIView!
    @IBOutlet weak var viewAddAddress: UIView!
    @IBOutlet weak var lblSavedAddressCount: UILabel!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var btnDeliverHere: UIButton!
    var addressArray = [JSON]()
    var id = Int()
    var selectedIndex = Int()
    var pageTypeFromCheckOut = String()
    var xibSelect = Bool()
    var radioSelect = Bool()
    var radioSlectArray = [Int]()
    var selectedAddress = [String:JSON]()
    var addressId = Int()
    var listCount = Int()
     let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    override func viewDidLoad() {
        super.viewDidLoad()
        

        viewAddAddress.addShadow2()
        tableView.addShadow2()
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
         self.navigationController?.setNavigationBarHidden(true, animated: true)
        if pageTypeFromCheckOut == "CheckOut" {
            self.lblTitle.text = "Select Address"
//            self.navigationController!.navigationBar.titleTextAttributes = [NSAttributedString.Key.font: UIFont(name: "hind-bold", size: 20)!]
            self.btnDeliverHere.isHidden = false
            self.btnDeliverHeight.constant = 50
            ApiCallToGetSavedList()
            
        }
        else  if pageTypeFromCheckOut == "Payment" {
            self.lblTitle.text = "Select Address"
//            self.navigationController!.navigationBar.titleTextAttributes = [NSAttributedString.Key.font: UIFont(name: "hind-bold", size: 20)!]
            self.btnDeliverHere.isHidden = false
            self.btnDeliverHeight.constant = 50
            ApiCallToGetSavedList()
        }
        else {
            ApiCallToGetSavedList()
            self.lblTitle.text = "My Addresses"
//            self.navigationController!.navigationBar.titleTextAttributes = [NSAttributedString.Key.font: UIFont(name: "hind-bold", size: 20)!]
            self.navigationController?.setNavigationBarHidden(true, animated: true)
            self.btnDeliverHere.isHidden = true
            self.btnDeliverHeight.constant = 0
        }
        
    }
    
    @IBAction func btnBackAction(_ sender: Any) {
          EditDeleteXib.removeFromSuperview()
        self.navigationController?.popViewController(animated: true)
    }
    
    
    @IBAction func btnDeliverHereAction(_ sender: Any) {
        if pageTypeFromCheckOut == "Payment" {
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "CCPaymentViewController") as! CCPaymentViewController
            let backButton = UIBarButtonItem()
            backButton.title = ""
            navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
            vc.defaultAddressDict1 = selectedAddress
            vc.addressSelect = "yes"
            self.navigationController?.pushViewController(vc, animated: true)
        }
        else {
            if selectedAddress.isEmpty == false {
                self.addressId = selectedAddress["id"]!.intValue
                ApiCallToCheckAddress()
            }
            else {
               createalert(title: "Alert", message: "Please select location", vc: self)
            }


        }
    }
    @IBAction func btnAddAddressAction(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveAddressViewController") as! SaveAddressViewController
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.pushViewController(vc, animated: true)
    }
    @objc func deleteBtnAction() {
        EditDeleteXib.removeFromSuperview()
        xibSelect = false
        ApiCallToDeleteSavedAddress()
    }
    @objc func editBtnAction() {
        EditDeleteXib.removeFromSuperview()
        xibSelect = false
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveAddressViewController") as! SaveAddressViewController
        vc.pageType = "Edit"
        vc.listCount1 = listCount
        let dict = addressArray[selectedIndex].dictionaryValue
        print(dict)
        vc.savedDict = dict
        self.navigationController?.pushViewController(vc, animated: true)
    }
    @objc func btnEditOrDeleteActio(sender: UIButton) {
        let addressDict = addressArray[sender.tag].dictionaryValue
        self.id = addressDict["id"]!.intValue
        var superview = sender.superview
        while let view = superview, !(view is UITableViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UITableViewCell else {
            // print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = tableView.indexPath(for: cell) else {
            // print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? SaveListTableViewCell else {
            //  print("rferffddvd")
            return
        }
        
        if let frame = cell1.superview?.convert(cell1.frame, to: nil) {
            print(frame)
            let xPosition = frame.size.width - 180
            requestEditDeleteViewGlobal(vc: self, yPosition: frame.origin.y + 10, xPoaition: xPosition)
            selectedIndex = sender.tag
            EditDeleteXib.btnDelete.addTarget(self, action: #selector(deleteBtnAction), for: .touchUpInside)
            EditDeleteXib.btnEdit.addTarget(self, action: #selector(editBtnAction), for: .touchUpInside)
            EditDeleteXib.layer.shadowColor = UIColor.black.cgColor
            EditDeleteXib.layer.shadowOpacity = 1
            EditDeleteXib.layer.shadowOffset = .zero
            EditDeleteXib.layer.cornerRadius = 5
            EditDeleteXib.layer.shadowRadius = 1
            EditDeleteXib.layer.shadowPath = UIBezierPath(rect: EditDeleteXib.bounds).cgPath
            EditDeleteXib.layer.shouldRasterize = true
            EditDeleteXib.layer.rasterizationScale = UIScreen.main.scale
            xibSelect = true
        }
        
    }
    
    func ApiCallToCheckAddress() {
        var params = [String:Any]()
        params["address_id"] = self.addressId
        var headers = [String : Any]()
            let auth = UserDefaults.standard.value(forKey: "token") as! String
            headers = ["Authorization": "Token \(auth)","Content-Type": "application/json" , "WAREHOUSE" : "\(wareHouseId)","WID":"1"]
        postMethodCustomHeader(apiName: "select-address/", params: params, vc: self, header: headers) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                if response["warehouseMatch"].stringValue == "y" {
                let vc = self.storyboard?.instantiateViewController(withIdentifier: "DeliveryDetailsViewController") as! DeliveryDetailsViewController
                 let backButton = UIBarButtonItem()
                 backButton.title = ""
                self.navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
                vc.defaultAddressDict = self.selectedAddress
                vc.addressSelect = "yes"
                vc.addressID = self.addressId
                self.navigationController?.pushViewController(vc, animated: true)
                }
                else {
                    createalert(title: "Alert", message: response["message"].stringValue, vc: self)
                }
            }
            else {
            }
        }
    }
    
    func ApiCallToGetSavedList() {
        getMethodWithAuthorizationReturnJsonWithoutDeviceId(apiName: "delivery-address/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.addressArray = response["data"].arrayValue
                self.listCount = self.addressArray.count
                self.lblSavedAddressCount.text = "\(self.addressArray.count) SAVED ADDRESSES"
                self.tableView.delegate = self
                self.tableView.dataSource = self
                self.tableView.reloadData()
            }
            else {
                 self.listCount = 0
                self.lblSavedAddressCount.text = "No Address Saved Yet"
                self.tableView.delegate = self
                self.tableView.dataSource = self
                self.tableView.reloadData()
//                createalert(title: "Alert", message: "Unable to fetch saved addresses", vc: self)
            }
        }
    }
    
    func ApiCallToDeleteSavedAddress() {
        getMethodWithAuthorizationReturnJsonWithoutDeviceId(apiName: "delete-address/\(self.id)/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.addressArray.removeAll()
                self.ApiCallToGetSavedList()
                self.tableView.reloadData()
            }
            else {
                createalert(title: "Alert", message: "Unable to fetch saved addresses", vc: self)
            }
        }
    }
}
extension SavedAdressListViewController : UITableViewDelegate , UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return addressArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "SaveListTableViewCell", for: indexPath) as! SaveListTableViewCell
        let addressDict = addressArray[indexPath.row].dictionaryValue
        cell.lblName.text = addressDict["delivery_name"]!.stringValue
        cell.lblArea.text = addressDict["delivery_street_address"]!.stringValue + " " + addressDict["billing_landmark"]!.stringValue
        cell.lblCountry.text = addressDict["delivery_state_name"]!.stringValue + " " + addressDict["delivery_country_name"]!.stringValue
        cell.lblMobile.text = addressDict["delivery_phone"]!.stringValue
        if indexPath.row == 0 {
            cell.lblDefault.isHidden = false
        }
        else {
            cell.lblDefault.isHidden = true
          //  cell.lblDefault.layer.cornerRadius = cell.lblDefault.frame.height/2
        }
      
        cell.btneEditOrDelete.tag = indexPath.row
        cell.btneEditOrDelete.addTarget(self, action: #selector(btnEditOrDeleteActio), for: .touchUpInside)
        if pageTypeFromCheckOut == "CheckOut" {
            cell.btnAddressSelect.isHidden = false
            if radioSlectArray.contains(indexPath.row) {
                cell.btnAddressSelect.setImage(UIImage(named: "radio_select"), for: .normal)
                selectedAddress = addressDict
            }
            else {
                cell.btnAddressSelect.setImage(UIImage(named: "radio_unselect"), for: .normal)
            }
        }
        else  if pageTypeFromCheckOut == "Payment" {
            cell.btnAddressSelect.isHidden = false
            if radioSlectArray.contains(indexPath.row) {
                cell.btnAddressSelect.setImage(UIImage(named: "radio_select"), for: .normal)
                selectedAddress = addressDict
            }
            else {
                cell.btnAddressSelect.setImage(UIImage(named: "radio_unselect"), for: .normal)
            }
        }
        else {
            cell.btnAddressSelect.isHidden = true
        }
        return cell
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 110
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if xibSelect == true {
            EditDeleteXib.removeFromSuperview()
            xibSelect = false
        }
        else {
            if radioSlectArray.contains(indexPath.row) {
                radioSlectArray.removeLast()
                tableView.reloadData()
                
            }
            else {
                if radioSlectArray.count != 0 {
                    radioSlectArray.removeAll()
                    radioSlectArray.append(indexPath.row)
                    tableView.reloadData()
                }
                else {
                    radioSlectArray.append(indexPath.row)
                    tableView.reloadData()
                }
                
            }
        }
        
    }
    
    
}
