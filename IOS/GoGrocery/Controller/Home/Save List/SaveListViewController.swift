//
//  SaveListViewController.swift
//  GoGrocery
//
//  Created by Shanu on 19/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class SaveListViewController: UIViewController {
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var btnCreate: UIButton!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var txtName: UITextField!
    var saveListArr = [JSON]()
    var productIdInSave = Int()
    var nameInsave = String()
    @IBOutlet weak var viewCreateList: UIView!
    @IBOutlet weak var viewCreateAndAdd: UIView!
    var productId = 0
    @IBOutlet weak var editPopupView: UIView!
    @IBOutlet weak var editContainerView: UIView!
    @IBOutlet weak var editButton: UIButton!
    @IBOutlet weak var deleteButton: UIButton!
    var saveListName = ""
    var saveListId = 0
    var isEditingList = false
    var isFromMySaveList = false
    
    @IBOutlet weak var addNewButton: UIButton!
    @IBOutlet weak var headerLabel: UILabel!
    @IBOutlet weak var addListViewHeight: NSLayoutConstraint!
    @IBOutlet weak var createListLabelHeight: NSLayoutConstraint!
    override func viewDidLoad() {
        super.viewDidLoad()
        
        txtName.delegate = self
        txtName.layer.cornerRadius = 5
        txtName.setLeftPaddingPoints(10)
        btnCreate.layer.cornerRadius = 5
        print(productIdInSave)
        getSavedProductList()
        viewCreateList.addShadow2()
        viewCreateAndAdd.addShadow2()
        nametxtInActive()
        // Do any additional setup after loading the view.
        editContainerView.alpha = 0
        editPopupView.dropShadow()
        let tap = UITapGestureRecognizer(target: self, action: #selector(self.handleTap(_:)))
        editContainerView.addGestureRecognizer(tap)
        editButton.titleEdgeInsets.left = 10
        deleteButton.titleEdgeInsets.left = 10
        
        addNewButton.layer.cornerRadius = 6
        addNewButton.clipsToBounds = true
        addNewButton.layer.borderWidth = 1
        addNewButton.layer.borderColor = UIColor.red.cgColor
        checkComeFromSaveList()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        navigationController?.setNavigationBarHidden(true, animated: true)
    }
    
    func checkComeFromSaveList() {
        if isFromMySaveList == true {
            addListViewHeight.constant = 0
            createListLabelHeight.constant = 0
            viewCreateList.alpha = 0
            viewCreateAndAdd.alpha = 0
            addNewButton.alpha = 1
            headerLabel.text = "My Save List"
        } else {
            addNewButton.alpha = 0
            headerLabel.text = "Save To List"
        }
    }
    
    @objc func handleTap(_ sender: UITapGestureRecognizer? = nil) {
        editContainerView.alpha = 0
    }
    
    @IBAction func backButtonTapped(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    
    @IBAction func addNewButtonTapped(_ sender: Any) {
        addListViewHeight.constant = 180
        createListLabelHeight.constant = 40
        viewCreateList.alpha = 1
        viewCreateAndAdd.alpha = 1
        addNewButton.alpha = 0
        if isEditingList == true {
            isEditingList = false
            self.txtName.text = ""
            self.btnCreate.setTitle("CREATE & ADD", for: .normal)
        }
    }
    
    @IBAction func btnCreateAction(_ sender: Any) {
       if txtName.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter name", vc: self)
        }
       else {
        if isEditingList == true {
            editSavedList()
        } else {
            self.saveListName = txtName.text!
            if isFromMySaveList == true {
                apiCallToCreateNewEmptyList()
            } else {
                ApiCallToSaveProduct()
            }
            
        }
        
        }
    }
    
    @IBAction func editTapped(_ sender: Any) {
        isEditingList = true
        
        self.btnCreate.setTitle("UPDATE", for: .normal)
        self.txtName.text = self.saveListName
        nametxtActive()
        editContainerView.alpha = 0
        print("edit")
        addListViewHeight.constant = 180
        createListLabelHeight.constant = 40
        viewCreateList.alpha = 1
        viewCreateAndAdd.alpha = 1
        addNewButton.alpha = 1
    }
    
    
    @IBAction func deleteTapped(_ sender: Any) {
         print("delete")
        editContainerView.alpha = 0
        deleteSavedList()
    }
    
    
    //    MARK:- Active
    func nametxtActive() {
        self.txtName.layer.borderColor = UIColor(named: "textBorderColor")?.cgColor
        self.txtName.layer.borderWidth = 1
        self.lblName.isHidden = false
    }
    func nametxtInActive() {
        txtName.layer.borderColor = UIColor.darkGray.cgColor
        txtName.layer.borderWidth = 1
        self.lblName.isHidden = true
    }
//    MARK:- Api Calling
    func ApiCallToSaveProduct() {
         var params = [String:Any]()
         params["website_id"] = 1
         params["product_id"] = "\(productId)"
         params["name"] = self.saveListName
         print(params)
         postMethodQueryWithAuthorization(apiName: "save-list/", params: params, vc: self) { (response : JSON) in
             print(response)
            if response["status"].intValue == 200 {
                if response["msg"].stringValue == "Exist" {
                    createalert(title: "Alert", message: "List name already exist", vc: self)
                } else {
                    self.getSavedProductList()
                    self.txtName.text = ""
                    self.nametxtInActive()
                }
                
            }
         }
     }
    func getSavedProductList() {
        getMethodWithAuthorizationReturnJson(apiName: "save-list/", vc: self) { (response : JSON) in
            print(response)
            if response["message"].stringValue == "Success" {
                self.saveListArr = response["data"].arrayValue
                self.tableView.delegate = self
                self.tableView.dataSource = self
                self.tableView.reloadData()
            }
            else {
                self.tableView.delegate = self
                self.tableView.dataSource = self
                self.tableView.reloadData()
            }
        }
    }
    
    func deleteSavedList() {
        deleteMethod(apiName: "addeditdelete-from-savelist/\(self.saveListId)/" , vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.getSavedProductList()
                createalert(title: "Alert", message: "Successfully deleted", vc: self)
            } else {
                createalert(title: "Alert", message: "Unable to delete save list", vc: self)
            }
        }
        
    }
    
    func editSavedList() {
        
        var params = [String:Any]()
        params["name"] = self.txtName.text!
        params["savelist_id"] = "\(self.saveListId)"
        
        print(params)
        putMethodReturnJson(apiName: "addeditdelete-from-savelist/", params: params , vc : self) { (response : JSON) in
      //  requestWithPut(methodName: "addeditdelete-from-savelist/", parameter: params) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.isEditingList = false
                self.txtName.text = ""
                self.btnCreate.setTitle("CREATE & ADD", for: .normal)
                self.addNewButton.alpha = 0
                self.nametxtInActive()
                self.getSavedProductList()
                let msg = response["message"].stringValue
                createalert(title: "Alert", message: "Successfully updated", vc: self)
            }
            else {
                let msg = response["message"].stringValue
                if msg == "list already exist" {
                    createalert(title: "Alert", message: msg, vc: self)
                } else {
                    createalert(title: "Alert", message: "Unable to update list", vc: self)
                }
                
            }
        }
    }
    
    func apiCalltoSaveInexistingList() {
        var params = [String:Any]()
        params["website_id"] = 1
        params["product_id"] = productId
        params["list_id"] = self.saveListId
        params["action"] = "add"
        print(params)
         putMethodReturnJson(apiName: "addremove-from-savelist/", params: params , vc : self) { (response : JSON) in
      //  requestWithPut(methodName: "addremove-from-savelist/", parameter: params) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                self.getSavedProductList()
                let msg = response["msg"].stringValue
                if msg == "Exist" {
                    createalert(title: "Alert", message: "Item already exist in list", vc: self)
                } else {
                    createalert(title: "Alert", message: "Successfully added", vc: self)
                }
            }
            else {
                createalert(title: "Alert", message: "Unable to add in list", vc: self)
            }
        }
    }
    
    func apiCallToCreateNewEmptyList() {
        var params = [String:Any]()
        params["website_id"] = 1
        params["name"] = self.saveListName
        print(params)
        postMethodQueryWithAuthorization(apiName: "addeditdelete-from-savelist/", params: params, vc: self) { (response : JSON) in
            print(response)
           if response["status"].intValue == 200 {
               if response["msg"].stringValue == "Exist" {
                   createalert(title: "Alert", message: "List name already exist", vc: self)
               } else {
                   self.getSavedProductList()
                   self.txtName.text = ""
                   self.nametxtInActive()
               }
               
           } else {
                let msg = response["message"].stringValue
                if msg == "list already exist" {
                    createalert(title: "Alert", message: "List name already exist", vc: self)
                } else {
                    createalert(title: "Alert", message: "Unable to add list. Please try after sometime", vc: self)
                }
            }
        }
    }
    
    @objc func showMenu(sender: UIButton) {
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
        guard let cell1 = superview as? SaveTableViewCell else {
            //  print("rferffddvd")
            return
        }
        
        if let frame = cell1.superview?.convert(cell1.frame, to: nil) {
            let saveDict = saveListArr[indexPath.row].dictionaryValue
            self.saveListId = saveDict["id"]!.intValue
            self.saveListName = saveDict["savelist_name"]!.stringValue
            let x = frame.width - self.editPopupView.frame.width - 5
            let y = frame.origin.y + 10
            self.editContainerView.alpha = 1
            self.editPopupView.frame = CGRect(x: x, y: y, width: self.editPopupView.frame.width, height: self.editPopupView.frame.height)
            
        }
        
        
        
    }
    
}
extension SaveListViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == txtName {
            nametxtActive()
        }
//        else {
//            nametxtInActive()
//        }
    }
    func textFieldDidEndEditing(_ textField: UITextField, reason: UITextField.DidEndEditingReason) {
        if textField == txtName {
            nametxtInActive()
        }
    }
    
}
extension SaveListViewController: UITableViewDelegate, UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.saveListArr.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "SaveTableViewCell", for: indexPath) as! SaveTableViewCell
        let saveDict = saveListArr[indexPath.row].dictionaryValue
        print(saveDict)
        cell.btnEdit.tag = indexPath.row
        cell.btnEdit.addTarget(self, action: #selector(showMenu), for: .touchUpInside)
        cell.lblName.text = saveDict["savelist_name"]?.stringValue
        cell.lblItemCount.text = "\(saveDict["count"]!.stringValue) Items"
        let dateString = "\(saveDict["modified"]!.stringValue)"
        //let dateString = "Thu, 22 Oct 2015 07:45:17 +0000"
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
        dateFormatter.locale = Locale.init(identifier: "en_GB")
        let dateObj = dateFormatter.date(from: dateString)
        dateFormatter.dateFormat = "MM/dd/yyyy"
        print("Dateobj: \(dateFormatter.string(from: dateObj!))")
        cell.lblDate.text = "\(dateFormatter.string(from: dateObj!))"
        
        cell.addShadow2()
        cell.selectionStyle = .none
        return cell
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 85
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let saveDict = saveListArr[indexPath.row].dictionaryValue
        if isFromMySaveList == false {
            //self.saveListName = saveDict["savelist_name"]!.stringValue
            self.saveListId = saveDict["id"]!.intValue
            apiCalltoSaveInexistingList()
        } else {
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "SaveListDetailsViewController") as! SaveListDetailsViewController
            vc.listSlug = saveDict["slug"]!.stringValue
            vc.listId = saveDict["id"]!.intValue
            self.navigationController?.pushViewController(vc, animated: true)
        }
        
    }
    
    
}
extension UIView {

    func dropShadow() {
        self.layer.masksToBounds = false
        self.layer.shadowColor = UIColor.black.cgColor
        self.layer.shadowOpacity = 0.6
        self.layer.shadowOffset = CGSize(width: -1, height: 1)
        self.layer.shadowRadius = 2
        self.layer.shadowPath = UIBezierPath(rect: self.bounds).cgPath
        self.layer.shouldRasterize = true
        self.layer.rasterizationScale = UIScreen.main.scale

    }
}

