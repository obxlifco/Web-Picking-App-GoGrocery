//
//  SaveAddressViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 29/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//


import UIKit
import SwiftyJSON
import Alamofire
class SaveAddressViewController: UIViewController  {
    
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var lblApartment: UILabel!
    @IBOutlet weak var lblEmirates: UILabel!
    @IBOutlet weak var lblArea: UILabel!
    @IBOutlet weak var lblMobile: UILabel!
    
    @IBOutlet weak var txtName: UITextField!
    @IBOutlet weak var txtApartment: UITextField!
    @IBOutlet weak var txtEmirates: UITextField!
    @IBOutlet weak var txtArea: UITextField!
    @IBOutlet weak var txtMobile: UITextField!
    
    @IBOutlet weak var btnCancel: UIButton!
    @IBOutlet weak var btnAdd: UIButton!
    @IBOutlet weak var btnDefaultAction: UIButton!
    @IBOutlet weak var viewAddCancel: UIView!
    
    @IBOutlet weak var lblCountryCode: UILabel!
    @IBOutlet weak var buttonCC: UIButton!
    @IBOutlet weak var lblCC: UILabel!
    @IBOutlet weak var mobileCCTable: UITableView!
    @IBOutlet weak var ccTableView: UIView!
    @IBOutlet weak var ccBackgroundView: UIView!
    @IBOutlet weak var lblTitle: UILabel!
    @IBOutlet weak var navigationView: UIView!
    
    var pageType = String()
    var pageTypeFrom = String()
    var defaluSelectBool = Bool()
    var stateID = Int()
    var id = Int()
    var cID = Int()
    var checkID = Int()
    var savedDict = [String:JSON]()
    var ccCode = ["50","52","53","54","55","56","58"]
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var listCount1 = Int()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //        getStateList()
        viewAddCancel.addShadow1()
        navigationView.addShadow1()
        ccTableView.layer.cornerRadius = 5
        defaluSelectBool = false
        allInActive()
        self.btnCancel.layer.borderColor = UIColor(named: "buttonColor")?.cgColor
        self.btnCancel.layer.borderWidth = 1
        self.btnCancel.layer.cornerRadius = 5
        self.btnAdd.layer.cornerRadius = 5
        viewAddCancel.addShadow2()
        
        
        txtName.delegate = self
        txtApartment.delegate = self
        txtEmirates.delegate = self
        txtArea.delegate = self
        txtMobile.delegate = self
        
        txtName.layer.cornerRadius = 5
        txtApartment.layer.cornerRadius = 5
        txtEmirates.layer.cornerRadius = 5
        txtArea.layer.cornerRadius = 5
        txtMobile.layer.cornerRadius = 5
        
        txtName.setLeftPaddingPoints(10)
        txtApartment.setLeftPaddingPoints(10)
        txtEmirates.setLeftPaddingPoints(10)
        txtArea.setLeftPaddingPoints(10)
        txtMobile.setLeftPaddingPoints(10)
        if self.pageType == "Add" {
            
        }
        
        ccBackgroundView.alpha = 0
        ccTableView.alpha = 0
        lblCountryCode.layer.cornerRadius = 5
        lblCountryCode.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        lblCountryCode.layer.borderWidth = 2
        buttonCC.titleEdgeInsets.left = 10
        buttonCC.layer.cornerRadius = 5
        let tap = UITapGestureRecognizer(target: self, action: #selector(self.handleTap(_:)))
        ccBackgroundView.addGestureRecognizer(tap)
        
        //        btnDefaultAction.addTarget(self, action: #selector(btnDefaultActionaction), for: .touchUpInside)
        
        
        // Do any additional setup after loading the view.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.setNavigationBarHidden(true, animated: true)
        if self.pageType == "Edit" {
            self.lblTitle.text = "Edit Address"
          //  self.navigationController!.navigationBar.titleTextAttributes = [NSAttributedString.Key.font: UIFont(name: "hind-bold", size: 20)!]
            getSavedData()
        }
        else
        {
            self.lblTitle.text  = "Add a New Address "
           // self.navigationController!.navigationBar.titleTextAttributes = [NSAttributedString.Key.font: UIFont(name: "hind-bold", size: 20)!]
            //            getSavedData()
        }
        
    }
    
    @IBAction func btnBackAction(_ sender: Any) {
         if pageTypeFrom == "Cart" {
             let viewControllers: [UIViewController] = self.navigationController!.viewControllers
             for aViewController in viewControllers {
                 if aViewController is CartViewController {
                     self.navigationController!.popToViewController(aViewController, animated: true)
                 }
             }
         }
         else {
             
              self.navigationController?.popViewController(animated: true)
         }
        
    }
    
    
    @IBAction func ccButtontapped(_ sender: Any) {
        ccActive()
        ccBackgroundView.alpha = 1
        ccTableView.alpha = 1
    }
    @objc func handleTap(_ sender: UITapGestureRecognizer? = nil) {
        print("handletap")
        ccInActive()
        UIView.animate(withDuration: 0.3, delay: 0.0, options: [], animations: {
            self.ccBackgroundView.alpha = 0
            self.ccTableView.alpha = 0
           
        })
    }
    func ccActive() {
        self.buttonCC.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "CC" {
            self.buttonCC.setTitle("", for: .normal)
        }
        
        self.lblCC.isHidden = false
    }
    func ccInActive() {
        buttonCC.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "" {
            self.buttonCC.setTitle("CC", for: .normal)
            self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        }
        
        self.lblCC.isHidden = true
    }
    
    func  getSavedData() {
        allInActive()
        self.txtName.text = savedDict["delivery_name"]!.stringValue
      
        nametxtTempActive()
        self.txtApartment.text = savedDict["delivery_street_address"]!.stringValue
        apartmenttxtTempActive()
        self.txtArea.text = savedDict["billing_landmark"]!.stringValue
        areatxtTempActive()
        self.txtEmirates.text = savedDict["delivery_state_name"]!.stringValue
        emiratestxtTempActive()
        //self.txtMobile.text = savedDict["delivery_phone"]!.stringValue
        mobiletxtTempActive()
        let mobileNo = savedDict["delivery_phone"]!.stringValue
        print(mobileNo)
       // if mobileNo.count == 12 {
            self.txtMobile.text = String((savedDict["delivery_phone"]!.stringValue).dropFirst(5))
            let Code = "\(String(Array(mobileNo)[3]))\(String(Array(mobileNo)[4]))"
            if self.ccCode.contains(Code) {
                self.buttonCC.setTitle(Code, for: .normal)
                self.buttonCC.setTitleColor(.black, for: .normal)
            }
        //}
//        else {
//            print(String((savedDict["delivery_phone"]!.stringValue).dropFirst(5)))
//            self.txtMobile.text = String((savedDict["delivery_phone"]!.stringValue).dropFirst(5))
//        }
        // self.id = addressDict["id"]!.intValue
        self.cID = savedDict["id"]!.intValue
        if savedDict["delivery_state_name"]!.stringValue == "Abu Dhabi" {
            self.stateID =  155
        }
        if savedDict["delivery_state_name"]!.stringValue == "Dubai" {
            self.stateID =  156
        }
        if savedDict["delivery_state_name"]!.stringValue == "Ajman" {
            self.stateID =  157
        }
        if savedDict["delivery_state_name"]!.stringValue == "Sharjah" {
            self.stateID =  158
        }
        if savedDict["delivery_state_name"]!.stringValue == "Fujairah" {
            self.stateID =  159
        }
        if savedDict["delivery_state_name"]!.stringValue == "Ras Al Khaimah" {
            self.stateID =  160
        }
        
         if listCount1 == 1 {
            btnDefaultAction.setImage(UIImage(named: "radio_select"), for: .normal)
            self.checkID = 1
            defaluSelectBool = true
            btnDefaultAction.isUserInteractionEnabled = false
        }
         else {
            if savedDict["set_primary"]?.intValue == 1 {
                 btnDefaultAction.setImage(UIImage(named: "radio_select"), for: .normal)
                 self.checkID = 1
                 defaluSelectBool = true
             }
            
             else {
                 btnDefaultAction.setImage(UIImage(named: "radio_unselect"), for: .normal)
                 self.checkID = 0
                 defaluSelectBool = false
             }
        }
    }
    //    MARK:- Temp Active
    
    func nametxtTempActive() {
        
        self.txtName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtName.layer.borderWidth = 1
        self.lblName.isHidden = false
        self.lblName.textColor = UIColor(named: "inactiveText")
    }
    func apartmenttxtTempActive() {
        
        self.txtApartment.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtApartment.layer.borderWidth = 1
        self.lblApartment.isHidden = false
        self.lblApartment.textColor = UIColor(named: "inactiveText")
    }
    
    func emiratestxtTempActive() {
        self.txtEmirates.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtEmirates.layer.borderWidth = 1
        self.lblEmirates.isHidden = false
        self.lblEmirates.textColor = UIColor(named: "inactiveText")
    }
    
    func areatxtTempActive() {
        self.txtArea.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtArea.layer.borderWidth = 1
        self.lblArea.isHidden = false
        self.lblArea.textColor = UIColor(named: "inactiveText")
    }
    func mobiletxtTempActive() {
        self.txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtMobile.layer.borderWidth = 1
        self.lblMobile.isHidden = false
        self.lblMobile.textColor = UIColor(named: "inactiveText")
    }
    
    
    //    MARK:- Active
    func nametxtActive() {
        self.txtName.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtName.layer.borderWidth = 2
        self.lblName.textColor = UIColor(named: "buttonBackgroundColor")
        self.lblName.isHidden = false
    }
    func apartmenttxtActive() {
        self.txtApartment.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtApartment.layer.borderWidth = 2
        self.lblApartment.textColor = UIColor(named: "buttonBackgroundColor")
        self.lblApartment.isHidden = false
    }
    func emiratestxtActive() {
        self.txtEmirates.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtEmirates.layer.borderWidth = 2
        self.lblEmirates.textColor = UIColor(named: "buttonBackgroundColor")
        self.lblEmirates.isHidden = false
    }
    func areatxtActive() {
        self.txtArea.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtArea.layer.borderWidth = 2
        self.lblArea.textColor = UIColor(named: "buttonBackgroundColor")
        self.lblArea.isHidden = false
    }
    func mobiletxtActive() {
        self.txtMobile.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtMobile.layer.borderWidth = 2
        self.lblMobile.textColor = UIColor(named: "buttonBackgroundColor")
        self.lblMobile.isHidden = false
    }
    //    MARK:- Inactive
    func nametxtInActive() {
        txtName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtName.layer.borderWidth = 1
        self.lblName.isHidden = true
    }
    func apartmenttxtInActive() {
        txtApartment.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtApartment.layer.borderWidth = 1
        self.lblApartment.isHidden = true
    }
    func emiratestxtInActive() {
        txtEmirates.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmirates.layer.borderWidth = 1
        self.lblEmirates.isHidden = true
    }
    func areaInActive() {
        txtArea.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtArea.layer.borderWidth = 1
        self.lblArea.isHidden = true
    }
    func mobileInActive() {
        txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtMobile.layer.borderWidth = 1
        self.lblMobile.isHidden = true
    }
    //    MARK:- All Inactive
    func allInActive() {
        txtName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtName.layer.borderWidth = 1
        self.lblName.isHidden = true
        
        txtApartment.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtApartment.layer.borderWidth = 1
        self.lblApartment.isHidden = true
        
        txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtMobile.layer.borderWidth = 1
        lblMobile.isHidden = true
        
        txtEmirates.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmirates.layer.borderWidth = 1
        self.lblEmirates.isHidden = true
        
        txtArea.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtArea.layer.borderWidth = 1
        self.lblArea.isHidden = true
        
        buttonCC.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "" {
            self.buttonCC.setTitle("CC", for: .normal)
            self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        } else {
            self.buttonCC.setTitleColor(.black, for: .normal)
        }
        //self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        lblCC.isHidden = true
    }
    
    
    @IBAction func btnSlectAction(_ sender: Any) {
        setUpUpdateOrderXibFunc ()
    }
    @IBAction func btnAddAction(_ sender: Any) {
        if txtName.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter email", vc: self)
        }
        else  if txtApartment.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your apartment", vc: self)
        }
        else  if txtEmirates.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your city", vc: self)
        }
        else  if txtArea.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your area", vc: self)
        }
        else  if txtMobile.text!.trimmingCharacters(in: .whitespaces).count < 7 {
            createalert(title: "Alert", message: "Please enter valid mobile number", vc: self)
        }
        else if buttonCC.currentTitle == "CC" {
            createalert(title: "Alert", message: "Please enter your mobile CC", vc: self)
        }
        else {
            if self.pageType == "Edit" {
                ApiCallToEditAddress()
            }
            else {
                ApiCallToSaveAddress()
            }
            
        }
    }
    
    @IBAction func btnCancelAction(_ sender: Any) {
        if pageTypeFrom == "Cart" {
            let viewControllers: [UIViewController] = self.navigationController!.viewControllers
            for aViewController in viewControllers {
                if aViewController is CartViewController {
                    self.navigationController!.popToViewController(aViewController, animated: true)
                }
            }
        }
        else {
            
             self.navigationController?.popViewController(animated: true)
        }
       
    }
    
    @IBAction func defaultSelectAction(_ sender: Any) {
        if defaluSelectBool == false {
            btnDefaultAction.setImage(UIImage(named: "radio_select"), for: .normal)
            self.checkID = 1
            defaluSelectBool = true
        }
        else {
            btnDefaultAction.setImage(UIImage(named: "radio_unselect"), for: .normal)
            self.checkID = 0
            defaluSelectBool = false
        }
        
    }
    
    func setUpUpdateOrderXibFunc () {
        requestLocationViewGlobal(vc: self)
        LocationXib.btnAbuDhabi.addTarget(self, action: #selector(btnAbuDhabiAction), for: .touchUpInside)
        LocationXib.btnDubai.addTarget(self, action: #selector(btnDubaiAction), for: .touchUpInside)
        LocationXib.btnAjman.addTarget(self, action: #selector(btnAjmanAction), for: .touchUpInside)
        LocationXib.btnSarjah.addTarget(self, action: #selector(btnSarjahAction), for: .touchUpInside)
        LocationXib.btnFujairah.addTarget(self, action: #selector(btnFujairahAction), for: .touchUpInside)
        LocationXib.btnRasAl.addTarget(self, action: #selector(btnRasAlAction), for: .touchUpInside)
    }
    
    
    @objc func btnAbuDhabiAction () {
        
        LocationXib.removeFromSuperview()
        self.txtEmirates.text = "Abu Dhabi"
        self.stateID =  155
        emiratestxtInActive()
    }
    
    @objc func btnDubaiAction () {
        LocationXib.removeFromSuperview()
        self.txtEmirates.text = "Dubai"
        self.stateID =  156
        emiratestxtInActive()
    }
    
    @objc func btnAjmanAction () {
        LocationXib.removeFromSuperview()
        self.txtEmirates.text = "Ajman"
        self.stateID =  157
        emiratestxtInActive()
    }
    
    @objc func btnSarjahAction () {
        LocationXib.removeFromSuperview()
        self.txtEmirates.text = "Sharjah"
        self.stateID =  158
        emiratestxtInActive()
    }
    
    @objc func btnFujairahAction () {
        LocationXib.removeFromSuperview()
        self.txtEmirates.text = "Fujairah"
        self.stateID =  159
        emiratestxtInActive()
    }
    @objc func btnRasAlAction () {
        LocationXib.removeFromSuperview()
        self.txtEmirates.text = "Ras Al Khaimah"
        self.stateID =  160
        emiratestxtInActive()
    }
    @objc func btnDefaultActionaction(sender: UIButton) {
        
    }
    func ApiCallToSaveAddress(){
        let mobileNo = "971\(buttonCC.currentTitle!)\(txtMobile.text!)"
        var params = [String:Any]()
        params["address"] = self.txtApartment.text!
        params["area"] = self.txtArea.text
        params["check"] = checkID
        params["country"] = 221
        params["mobile_no"] = mobileNo
        params["name"] = self.txtName.text!
        params["state"] = self.stateID
        params["carrier_code"] = Int(buttonCC.currentTitle!.trimmingCharacters(in: .whitespaces)) ?? 00
        print(params)
        
//        var headers = [String : Any]()
//            let auth = UserDefaults.standard.value(forKey: "token") as! String
//            headers = ["Authorization": "Token \(auth)","Content-Type": "application/json" , "WAREHOUSE" : "\(wareHouseId)"]
//        print(headers)
//        postMethodCustomHeader(apiName: "select-address/", params: params, vc: self, header: headers) { (response : JSON) in
        postMethodQuerySave(apiName: "delivery-address/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.showAlert21(message: response["message"].stringValue)
            }
            else {
                createalert(title: "Alert", message: "Error in saving address", vc: self)
            }
        }
    }
    func ApiCallToEditAddress() {
        let mobileNo = "971\(buttonCC.currentTitle!)\(txtMobile.text!)"
        var params = [String:Any]()
        params["customers_addressId"] = self.cID
        params["address"] = self.txtApartment.text!
        params["area"] = self.txtArea.text
        params["check"] = checkID
        params["country"] = 221
        params["mobile_no"] = mobileNo
        params["name"] = self.txtName.text!
        params["state"] = self.stateID
        params["carrier_code"] = Int(buttonCC.currentTitle!.trimmingCharacters(in: .whitespaces)) ?? 00
        print(params)
//        var headers = [String : Any]()
//        let auth = UserDefaults.standard.value(forKey: "token") as! String
//        headers = ["Authorization": "Token \(auth)","Content-Type": "application/json" , "WAREHOUSE" : "\(wareHouseId)"]
    //    requestWithPutForEditAddress(methodName: "delivery-address/", parameter: params) { (response : JSON) in
        putMethodEdit(apiName: "delivery-address/", params: params, vc: self) { (response : JSON) in
            print(response)
            //            let successDict = response[0].dictionaryValue
            if response["status"].intValue == 200 {
                let msg = response["message"].stringValue
                self.showAlert22(message: msg)
            }
            else {
                createalert(title: "Alert", message: "Unable to update address", vc: self)
            }
        }
        
    }
    
    
    //    MARK:- Alert
    func showAlert21(message: String)
    {
        let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
            if self.pageType == "Cart" {
                let vc = self.storyboard?.instantiateViewController(withIdentifier: "DeliveryDetailsViewController") as! DeliveryDetailsViewController
                self.navigationController?.pushViewController(vc, animated: true)
            }
            else {
             self.navigationController?.popViewController(animated: true)
            }
            
        }))
        self.present(alert, animated: true, completion: nil)
    }
    func showAlert22(message: String)
    {
        let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
            self.navigationController?.popViewController(animated: true)
        }))
        self.present(alert, animated: true, completion: nil)
    }
    
}
extension SaveAddressViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == txtName {
            allInActive()
            nametxtActive()
        }
        else  if textField == txtApartment {
            
            //  nametxtInActive()
            allInActive()
            apartmenttxtActive()
        }
        else if textField == txtEmirates {
            allInActive()
            emiratestxtActive()
            setUpUpdateOrderXibFunc ()
        }
        else if textField == txtArea {
            allInActive()
            areatxtActive()
        }
        else {
            allInActive()
            mobiletxtActive()
        }
    }
    func textFieldDidEndEditing(_ textField: UITextField, reason: UITextField.DidEndEditingReason) {
        if textField == txtName {
            allInActive()
        }
        else if textField == txtApartment {
            allInActive()
        }
        else if textField == txtEmirates {
            allInActive()
        }
        else if textField == txtArea {
            allInActive()
        }
        else {
            allInActive()
        }
    }
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
        if textField == txtMobile {
            guard let text = textField.text else { return true }
            let newLength = text.count + string.count - range.length
            return newLength <= 7
        }
        return true
    }
}
// MARK:- CCTable data source and Delegate
extension SaveAddressViewController : UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return ccCode.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = mobileCCTable.dequeueReusableCell(withIdentifier: "MobileCCTableViewCell") as! MobileCCTableViewCell
        cell.ccLabel.text = ccCode[indexPath.row]
        cell.selectionStyle = .none
        return cell
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.buttonCC.setTitle(ccCode[indexPath.row], for: .normal)
        self.buttonCC.setTitleColor(.black, for: .normal)
        ccBackgroundView.alpha = 0
        ccTableView.alpha = 0
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 50
    }
    
}
