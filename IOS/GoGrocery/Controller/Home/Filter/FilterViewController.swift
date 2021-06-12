//
//  FilterViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 11/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
protocol SelectFilterDelegate: class {
    func filterSelect(catArr: [Int], isCategoryBool: Bool, isBrandSelect: Bool , brandArr: [Int],isFilterFromSearchElastic: Bool)
}
class FilterViewController: UIViewController {
    @IBOutlet weak var btnApply: UIButton!
    @IBOutlet weak var btnCancel: UIButton!
    @IBOutlet weak var tableView2: UITableView!
    @IBOutlet weak var tableView1: UITableView!
    var titleStringInFilter = String()
    var productTitleInFilter = String()
    var slugInListingInFilter = String()
    var typeInFilter = String()
    var filterArr = [JSON]()
    var childArr = [JSON]()
    var brandArayMustFilter = Array<Any>()
    var categoryArayMustFilter = Array<Any>()
    var brandIdArray = [Int]()
    var categoryIdArray = [Int]()
    var mainListIndex = 0
    var catBool = Bool()
    var brandBool = Bool()
    weak var delegate : SelectFilterDelegate?
    var filterArray = [JSON]()
    var savedCatID = [Int]()
    var savedBrandID = [Int]()
    var isBrandBool = Bool()
    var isCategoryBool = Bool()
    var isfirstTimeBool : Bool = true
    var isFilterFromSearch = Bool()
    var productIdArrayFromSearch = [Int]()
    var isBrandSelectInFilter = Bool()
    var isFirstTime: Bool = false
    var selectedMainFilter : Int = 0
    @IBOutlet weak var viewFilter: UIView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        catBool = true
        //   brandBool = false
        viewFilter.addShadow1()
        ApiCallToGetFilterData()
        btnApply.layer.cornerRadius = 5
        btnCancel.layer.cornerRadius = 5
        btnCancel.layer.borderColor = UIColor.red.cgColor
        btnCancel.layer.borderWidth = 1
//
//        btnApply.titleLabel!.font = UIFont(name: "hind-semibold", size: 14)
//        btnApply.titleLabel!.font = .boldSystemFont(ofSize: 14)
//
//        btnCancel.titleLabel!.font = UIFont(name: "hind-semibold", size: 14)
//        btnCancel.titleLabel!.font = .boldSystemFont(ofSize: 14)
        
    }
    override func viewWillAppear(_ animated: Bool) {
        if let slugInFilter = UserDefaults.standard.value(forKey: "slugInListingInFilter") as? String {
            if slugInFilter != slugInListingInFilter {
                self.categoryIdArray.removeAll()
                self.brandIdArray.removeAll()
            }
        }
        //        if isFilterFromSearch {}
        self.navigationController?.isNavigationBarHidden = true
        getSavedFilterData()
    }
    //    MARK:- Button Actions
    @IBAction func btnClearAction(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    @IBAction func btnBack(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    
    
    @IBAction func btnCancelAction(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    
    @IBAction func btnApplyAction(_ sender: Any) {
        var isfilterFromSearchBool = Bool()
        self.navigationController?.popViewController(animated: true)
        UserDefaults.standard.set(categoryIdArray, forKey: "category_Array")
        UserDefaults.standard.set(brandIdArray, forKey: "brand_Array")
        UserDefaults.standard.set(slugInListingInFilter, forKey: "slugInListingInFilter")
        UserDefaults.standard.synchronize()
        if brandIdArray.count != 0 {
            isBrandBool = true
        }
        if categoryIdArray.count != 0 {
            isCategoryBool = true
        }
        if isFilterFromSearch == true {
            isfilterFromSearchBool = true
        }
        else {
            isfilterFromSearchBool = false
        }
        print(brandIdArray)
        print(categoryIdArray)
        self.delegate?.filterSelect(catArr: categoryIdArray, isCategoryBool: isCategoryBool, isBrandSelect: isBrandBool, brandArr: brandIdArray , isFilterFromSearchElastic: isfilterFromSearchBool)
    }
    func getSavedFilterData() {
        categoryIdArray.removeAll()
        guard let savCat = UserDefaults.standard.value(forKey: "category_Array") as? [Int] else {
            return
        }
        print(savCat)
        categoryIdArray = savCat
        brandIdArray.removeAll()
        guard let savBrand = UserDefaults.standard.value(forKey: "brand_Array") as? [Int] else {
            return
        }
        print(savBrand)
        brandIdArray = savBrand
        print(savedCatID)
        print(savedBrandID)
        if savedBrandID.count != 0 {
            tableView1.reloadData()
            tableView2.reloadData()
        }
        if savedCatID.count != 0 {
            tableView1.reloadData()
            tableView2.reloadData()
        }
    }
    
    //    MARK:- Api call to get filter data
    func  ApiCallToGetFilterData() {
        let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
        if isFilterFromSearch {
            var encodedString = ""
            for (i,smallString) in productIdArrayFromSearch.enumerated()  {
                if i == productIdArrayFromSearch.count - 1 {
                    encodedString  = encodedString + "\(smallString)"
                }
                else {
                    encodedString  = encodedString + "\(smallString),"
                }
                
            }
            if let data = (encodedString).data(using: String.Encoding.utf8) {
                let base64 = data.base64EncodedString(options: Data.Base64EncodingOptions(rawValue: 0))
                print(base64)
                
                //                print(encodedString)
                let api = "search-filter/?v=\(base64)"
                getMethodWithAuthorizationReturnJsonForSearchFilter(apiName: api, vc: self) { (response : JSON) in
                    print(response)
                    if response.arrayValue.count != 0 {
                        self.filterArr = response.arrayValue
                        for index in self.filterArr{
                            if index["field_name"].stringValue == "categories" {
                                self.filterArray.append(index)
                            }
                            else if index["field_name"].stringValue == "brand" {
                                self.filterArray.append(index)
                            }
                            else {
                            }
                        }
                        self.childArr = self.filterArray[0]["child"].arrayValue
                        print(self.filterArray)
                        self.selectedMainFilter = 0
                        self.tableView1.delegate = self
                        self.tableView1.dataSource = self
                        self.tableView1.reloadData()
                        self.tableView2.delegate = self
                        self.tableView2.dataSource = self
                        self.tableView2.reloadData()
                    }
                    else {
                        
                    }
                    
                }
            }
        }
        else {
            var api = String()
            
            if isBrandSelectInFilter == true {
                api = "listing_filters/?slug=\(slugInListingInFilter)&type=brand&warehouse_id=\(wareHouseId)&website_id=1"
            }
            else {
                api = "listing_filters/?slug=\(slugInListingInFilter)&type=category&warehouse_id=\(wareHouseId)&website_id=1"
            }
            
            getMethodReturnJson(apiName: api, vc: self) { (response : JSON) in
                if response.arrayValue.count != 0 {
                    self.filterArr = response.arrayValue
                    for index in self.filterArr{
                        if index["field_name"].stringValue == "categories" {
                            self.filterArray.append(index)
                        }
                        else if index["field_name"].stringValue == "brand" {
                            self.filterArray.append(index)
                        }
                        else {
                        }
                    }
                    print(self.filterArray)
                    if self.filterArray.count != 0 {
                        
                        //  if self.filterArray[0]["message"].stringValue != "Category not found." {
                        
                        self.childArr = self.filterArray[0]["child"].arrayValue
                        print(self.filterArray)
                         self.selectedMainFilter = 0
                        self.tableView1.delegate = self
                        self.tableView1.dataSource = self
                        self.tableView1.reloadData()
                        self.tableView2.delegate = self
                        self.tableView2.dataSource = self
                        self.tableView2.reloadData()
                    }
                    else {
                        createalert(title: "Alert", message: "Category Not Found", vc: self)
                    }
                    
                }
            }
        }
        
    }
}
extension FilterViewController : UITableViewDelegate , UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if tableView == tableView1 {
            return filterArray.count
        }
        else if tableView == tableView2 {
            return childArr.count
        }
        return filterArray.count
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 50
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        var commonCell = UITableViewCell()
        if tableView == tableView1 {
            let cell = tableView.dequeueReusableCell(withIdentifier: "FilterCategoryTableViewCell", for: indexPath) as! FilterCategoryTableViewCell
            let text = filterArray[indexPath.row]["field_name"].stringValue
            cell.lblCategory.text? = text.uppercased()
//            cell.lblCategory.font = UIFont(name: "hind-regular", size: 18)
//            cell.lblCategory.font = .boldSystemFont(ofSize: 18)
            if indexPath.row ==  selectedMainFilter {
                cell.contentView.backgroundColor = #colorLiteral(red: 0.9137254902, green: 0.9137254902, blue: 0.9137254902, alpha: 1)
            }
            else {
                cell.contentView.backgroundColor = .white
            }
            commonCell = cell
        }
        else {
            let cell1 = tableView.dequeueReusableCell(withIdentifier: "FilterSubCategoryTableViewCell", for: indexPath) as! FilterSubCategoryTableViewCell
            cell1.lblSubCat.text = childArr[indexPath.row]["name"].stringValue
            
            if savedCatID.count != 0 {
                if savedCatID.contains(childArr[indexPath.row]["id"].intValue) {
                    cell1.btnSubCat.setImage(UIImage(named: "checkbox_select"), for: .normal)
                }
            }
            else {
                if catBool == true {
                    if categoryIdArray.contains(childArr[indexPath.row]["id"].intValue) {
                        cell1.btnSubCat.setImage(UIImage(named: "checkbox_select"), for: .normal)
                        
                    }
                    else {
                        cell1.btnSubCat.setImage(UIImage(named: "checkbox_unselect"), for: .normal)
                    }
                }
            }
            if savedBrandID.count != 0 {
                if savedBrandID.contains(childArr[indexPath.row]["id"].intValue) {
                    cell1.btnSubCat.setImage(UIImage(named: "checkbox_select"), for: .normal)
                    
                }
            }
            else {
                if brandBool == true {
                    if brandIdArray.contains(childArr[indexPath.row]["id"].intValue) {
                        cell1.btnSubCat.setImage(UIImage(named: "checkbox_select"), for: .normal)
                        
                    }
                    else {
                        cell1.btnSubCat.setImage(UIImage(named: "checkbox_unselect"), for: .normal)
                        
                    }
                }
            }
            commonCell = cell1
        }
        return commonCell
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if tableView == tableView1 {
            let cell = tableView.dequeueReusableCell(withIdentifier: "FilterCategoryTableViewCell") as! FilterCategoryTableViewCell
           // cell.backgroundColor = UIColor.darkGray
            
            if filterArray[indexPath.row]["field_name"].stringValue == "categories" {
                childArr.removeAll()
                childArr = filterArray[indexPath.row]["child"].arrayValue
                tableView2.delegate = self
                tableView2.dataSource = self
                mainListIndex = indexPath.row
                self.selectedMainFilter = 0
                self.tableView2.reloadData()
                self.tableView1.reloadData()
                catBool = true
                brandBool = false
                
            }
            else {
                childArr.removeAll()
                childArr = filterArray[indexPath.row]["child"].arrayValue
                tableView2.delegate = self
                tableView2.dataSource = self
                mainListIndex = indexPath.row
                self.selectedMainFilter = 1
                self.tableView2.reloadData()
                self.tableView1.reloadData()
                brandBool = true
                catBool = false
            }
        }
        else {
            if isFirstTime != true {
                UserDefaults.standard.removeObject(forKey: "category_Array")
                UserDefaults.standard.removeObject(forKey: "brand_Array")
                if filterArray[mainListIndex]["field_name"].stringValue == "categories" {
                    if categoryIdArray.count == 0 {
                        self.categoryIdArray.append(childArr[indexPath.row]["id"].intValue)
                        catBool = true
                        brandBool = false
                        tableView2.reloadData()
                    }
                    else {
                        if categoryIdArray.contains(childArr[indexPath.row]["id"].intValue)  {
                            self.categoryIdArray.removeAll(where: { $0 == childArr[indexPath.row]["id"].intValue })
                            catBool = true
                            brandBool = false
                            tableView2.reloadData()
                        }
                        else {
                            self.categoryIdArray.append(childArr[indexPath.row]["id"].intValue)
                            catBool = true
                            brandBool = false
                            tableView2.reloadData()
                        }
                    }
                }
                else {
                    if brandIdArray.count == 0 {
                        self.brandIdArray.append(childArr[indexPath.row]["id"].intValue)
                        brandBool = true
                        catBool = false
                        tableView2.reloadData()
                    }
                    else {
                        if brandIdArray.contains(childArr[indexPath.row]["id"].intValue)  {
                            self.brandIdArray.removeAll(where: { $0 == childArr[indexPath.row]["id"].intValue })
                            brandBool = true
                            catBool = false
                            tableView2.reloadData()
                        }
                        else {
                            self.brandIdArray.append(childArr[indexPath.row]["id"].intValue)
                            brandBool = true
                            catBool = false
                            tableView2.reloadData()
                        }
                    }
                }
            }
            else {
                print(filterArray[mainListIndex]["field_name"].stringValue)
                if filterArray[mainListIndex]["field_name"].stringValue == "categories" {
                    if categoryIdArray.count == 0 {
                        self.categoryIdArray.append(childArr[indexPath.row]["id"].intValue)
                        catBool = true
                        brandBool = false
                        tableView2.reloadData()
                    }
                    else {
                        if categoryIdArray.contains(childArr[indexPath.row]["id"].intValue)  {
                            self.categoryIdArray.removeAll(where: { $0 == childArr[indexPath.row]["id"].intValue })
                            catBool = true
                            brandBool = false
                            tableView2.reloadData()
                        }
                        else {
                            self.categoryIdArray.append(childArr[indexPath.row]["id"].intValue)
                            catBool = true
                            brandBool = false
                            tableView2.reloadData()
                        }
                    }
                }
                else {
                    if brandIdArray.count == 0 {
                        self.brandIdArray.append(childArr[indexPath.row]["id"].intValue)
                        brandBool = true
                        catBool = false
                        tableView2.reloadData()
                    }
                    else {
                        if brandIdArray.contains(childArr[indexPath.row]["id"].intValue)  {
                            self.brandIdArray.removeAll(where: { $0 == childArr[indexPath.row]["id"].intValue })
                            brandBool = true
                            catBool = false
                            tableView2.reloadData()
                        }
                        else {
                            self.brandIdArray.append(childArr[indexPath.row]["id"].intValue)
                            brandBool = true
                            catBool = false
                            tableView2.reloadData()
                        }
                    }
                    
                }
            }
        }
    }
}

