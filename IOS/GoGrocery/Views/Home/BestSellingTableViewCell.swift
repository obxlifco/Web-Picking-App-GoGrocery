//
//  BestSellingTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 06/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
protocol BestSellingSelectDelegate: class {
    func BestSellingTypeSelected(id: Int , slug : String , category_type : String, type : String)
}
class BestSellingTableViewCell: UITableViewCell ,UICollectionViewDelegate, UICollectionViewDataSource{
    @IBOutlet weak var bestSellingColView: UICollectionView!
     @IBOutlet weak var lblBestSelling: UILabel!
    var cellBestSellingArray = [JSON]()
    var screenSize: CGRect!
    var screenWidth: CGFloat!
    var screenHeight: CGFloat!
    var deviceID = String()
    var productId = Int()
    var quantity = Int()
    private let spacing:CGFloat = 1
    var count = Int()
    var cartDatafromDb = [AddcCart]()
    weak var delegate : BestSellingSelectDelegate?
    override func awakeFromNib() {
        super.awakeFromNib()
        
        //  DataBaseHelper.sharedInstance.deleteAll
//        lblBestSelling.font = .boldSystemFont(ofSize: 16)
        count = 0
        bestSellingColView.layer.cornerRadius = 5

    }
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // Configure the view for the selected state
    }
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return cellBestSellingArray.count
          return 0
    }
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "BestSellingCollectionViewCell", for: indexPath) as! BestSellingCollectionViewCell
     /*   cell.btnSave.tag = indexPath.row
        cell.btnSave.addTarget(self, action: #selector(savebtnAction), for: .touchUpInside)
        cell.btnAddtoCart.tag = indexPath.row
        cell.btnAddtoCart.addTarget(self, action: #selector(addToCartbtnAction), for: .touchUpInside)
        
        cell.btnPlus.tag = indexPath.row
        cell.btnPlus.addTarget(self, action: #selector(btnPlusAction), for: .touchUpInside)
        cell.btnMinus.tag = indexPath.row
        cell.btnMinus.addTarget(self, action: #selector(btnMinusAction), for: .touchUpInside)
        
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
        let cellBestSellingDict = cellBestSellingArray[indexPath.row].dictionaryValue
        if cellBestSellingDict["weight"]!.intValue == 0 {
            cell.lblProductWeight.isHidden = true
        }
        else {
            let weight = cellBestSellingDict["weight"]!.intValue
            cell.lblProductWeight.text = "\(String(describing: weight))g"
        }

        let productId = "\(cellBestSellingDict["stock_data"]!["product_id"].intValue)"
        for index in cartDatafromDb {
            if productId == index.product_id {
                if let quant = index.quantity {
                    let costt = index.cost!
                    //let costD = Double(costt)
                    let inttype: Int = Int(quant) ?? 0
                 //   print(inttype)
                    if inttype != 0 {
                        //   print(inttype)
                        DispatchQueue.main.async {
                            cell.btnAddtoCart.setTitle("\(inttype)", for: .normal)
//                            cell.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 12)
//                             cell.btnAddtoCart.titleLabel?.font = .boldSystemFont(ofSize: 12)
                            cell.btnAddtoCart.backgroundColor = .white
                            cell.btnAddtoCart.setTitleColor(.black, for: .normal)
                            cell.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                            cell.cartStack.layer.borderWidth = 1
                            //cell.plusMinusStack.addBackground(color: UIColor(named: "buttonBackgroundColor")!)
                            cell.lblOrignalPrice.text = "AED \(costt)"
                           // print(inttype)
                           // print(costt)
                          //  print(cell.lblOrignalPrice.text!)
                            cell.btnMinus.isHidden = false
                            cell.btnPlus.isHidden = false
                            cell.cartStack.layer.cornerRadius = 5
                             cell.cartStack.layer.masksToBounds =  false
                        }
                    }
                    else {
                        cell.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
//                        cell.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 16)
//                          cell.btnAddtoCart.titleLabel?.font = .boldSystemFont(ofSize: 16)
                         cell.btnAddtoCart.backgroundColor = .clear
                         cell.btnAddtoCart.setTitleColor(.white, for: .normal)
                        cell.btnMinus.isHidden = true
                        cell.btnPlus.isHidden = true
                         cell.cartStack.layer.cornerRadius = 5
                         cell.cartStack.layer.masksToBounds =  false
                    }
                }
            }
            else {
                cell.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                cell.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 12)
                  cell.btnAddtoCart.titleLabel?.font = .boldSystemFont(ofSize: 12)
                 cell.btnAddtoCart.backgroundColor = .clear
                 cell.btnAddtoCart.setTitleColor(.white, for: .normal)
                cell.btnMinus.isHidden = true
                cell.btnPlus.isHidden = true
                 cell.cartStack.layer.cornerRadius = 5
                 cell.cartStack.layer.masksToBounds =  false
            }
            
        }
        let productImagesArray = cellBestSellingDict["product_image"]?.arrayValue
        let imageDict = productImagesArray![0].dictionaryValue
        if let brandurl = imageDict["img"]?.stringValue{
            let fullUrl = IMAGE_PRODUCT_URL + brandurl
            let url = URL(string: fullUrl)
          //  print(url!)
            cell.imgDeals.sd_setImage(with: url!)
        }
        if let foodType = cellBestSellingDict["veg_nonveg_type"]?.stringValue {
            cell.btnVeg.isHidden = false
            if foodType == "Non Veg" {
                cell.btnVeg.setImage(UIImage(named: "veg"), for: .normal)
            }
            else {
                cell.btnVeg.setImage(UIImage(named: "nonveg"), for: .normal)
            }
        }
        else {
            cell.btnVeg.isHidden = true
        }
        if let titleString = cellBestSellingDict["name"]?.stringValue {
            cell.lblTitle.text = titleString
            cell.lblTitle.font = UIFont(name: "hind-semibold", size: 14)
            cell.lblTitle.font = .boldSystemFont(ofSize: 14)
        }
        else {
            cell.lblTitle.isHidden = true
        }
        let cost1 = cellBestSellingDict["new_default_price"]!.doubleValue
        cell.lblOrignalPrice.text = "AED \(cost1)"
        bestSellingColView.layer.masksToBounds = false
        bestSellingColView.layer.shadowRadius = 2
        bestSellingColView.layer.shadowOpacity = 0.5
        bestSellingColView.layer.shadowColor = UIColor.gray.cgColor
        bestSellingColView.layer.shadowOffset = CGSize(width: 0 , height:2) */
        
        return cell
    }
    
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
     /*   let cellBestSellingDict = cellBestSellingArray[indexPath.row].dictionaryValue
        let pageTitle = ""
        let productId = cellBestSellingDict["id"]!.intValue
        let slug = cellBestSellingDict["slug"]!.stringValue
//        self.bannerdelegate?.BannerTypeSelected(id: productId!, slug: "\(slug)", category_type: pageTitle, type : "121")
        self.delegate?.BestSellingTypeSelected(id: productId, slug: "\(slug)", category_type: pageTitle, type: "121")
//        self.delegate?.BannerTypeSelected(id: productId, slug: slug, category_type: pageTitle, type: "121")
 */
        
    }
    
//    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize{
//        return  CGSize(width: 160, height: 300)
//    }
//
    
    //    MARK:- Button Actions
    @objc func savebtnAction (sender: UIButton) {

         let cellBestSellingDict = cellBestSellingArray[sender.tag].dictionaryValue
       //  print(cellBestSellingDict)
        let productId = cellBestSellingDict["stock_data"]!["product_id"].intValue
        let name = cellBestSellingDict["name"]!.stringValue
        let dict = ["product_id": productId, "name" : name] as [String : Any]
            NotificationCenter.default.post(name: Notification.Name("saveBtNotification"), object: nil, userInfo: dict)
    }
    @objc func addToCartbtnAction (sender: UIButton) {
        /*
        //   if count == 0 {
        self.count = count + 1
        var superview = sender.superview
        while let view = superview, !(view is UICollectionViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UICollectionViewCell else {
           // print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = bestSellingColView.indexPath(for: cell) else {
           // print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? BestSellingCollectionViewCell else {
          //  print("rferffddvd")
            return
        }
        // We've got the index path for the cell that contains the button, now do something with it.
        
        //     cell1.btnAddtoCart.setTitle("\(self.count)", for: .normal)
        
        let cellBestSellingDict = cellBestSellingArray[sender.tag].dictionaryValue
       // print(cellBestSellingDict)
        productId = cellBestSellingDict["stock_data"]!["product_id"].intValue
        quantity = count
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
        params["device_id"] = deviceID
        params["product_id"] = productId
        params["quantity"] = quantity
       // print(params)
        postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
          //  print(response)
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
               // print(count1)
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
               // print(cost)
                let dict = ["cost":cost ,"product_id":"\(self.productId)","quantity":count] as [String : Any]
                cell1.btnAddtoCart.setTitle("\(count)", for: .normal)
//                cell1.btnAddtoCart.titleLabel!.font = UIFont(name: "hind-semibold", size: 12)
//                cell1.btnAddtoCart.titleLabel!.font = .boldSystemFont(ofSize: 16)
                cell1.lblOrignalPrice.text = "AED \(cost)"
                cell1.btnAddtoCart.backgroundColor = .white
                cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
//                UIColor(named: "buttonBackgroundColor")
                cell1.btnPlus.isHidden = false
                cell1.btnMinus.isHidden = false
            
                cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                cell1.cartStack.layer.borderWidth = 1
               //  cell1.plusMinusStack.addBackground(color: UIColor(named: "buttonBackgroundColor")!)
              //  print(dict)
                DataBaseHelper.sharedInstance.save(object: dict)
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
               // print(DataBaseHelper.sharedInstance.getCartData())
               // print(self.cartDatafromDb.count)
                self.count = 0
              //  cell1.btnAddtoCart.isUserInteractionEnabled = false
                cell1.cartStack.layer.cornerRadius = 5
                cell1.cartStack.clipsToBounds =  true
                NotificationCenter.default.post(name: Notification.Name("CartUpdate"), object: nil, userInfo: nil)
            }
            else {
                cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
                cell1.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 12)
                 cell1.btnAddtoCart.titleLabel?.font = .boldSystemFont(ofSize: 12)
                cell1.btnPlus.isHidden = true
                cell1.btnMinus.isHidden = true
             //   cell1.btnAddtoCart.isUserInteractionEnabled = true
                let msg = response["msg"].stringValue
                let userInfo = ["msg" : msg]
                cell1.cartStack.layer.cornerRadius = 5
                cell1.cartStack.clipsToBounds =  true
                NotificationCenter.default.post(name: Notification.Name("AddCartfailure"), object: nil, userInfo: userInfo)
                self.count = 0
            }
        }
        //}
        */
    }
    
    @objc func btnPlusAction (sender: UIButton) {
    /*    var newProductId = String()
        var newQuantity = Int()
        var checkBool = false
        var coreDataindex = Int()
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
     //   print(DataBaseHelper.sharedInstance.getCartData())
       // print(cartDatafromDb)
        var superview = sender.superview
        while let view = superview, !(view is UICollectionViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UICollectionViewCell else {
          //  print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = bestSellingColView.indexPath(for: cell) else {
           // print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? BestSellingCollectionViewCell else {
           // print("rferffddvd")
            return
        }
        // We've got the index path for the cell that contains the button, now do something with it.
        
        let cellBestSellingDict = cellBestSellingArray[sender.tag].dictionaryValue
        print(cellBestSellingDict)
        let productId = "\(cellBestSellingDict["stock_data"]!["product_id"].intValue)"
        
        for (index, element) in cartDatafromDb.enumerated() {
            print("Item \(index): \(element)")
            var prouctId1 = element.product_id!
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                let quantt = element.quantity!
                let quant1 = quantt
              //  print(quant1)
                var inttype: Int = Int(quantt)!
              //  print(inttype)
                
                if inttype > 0 {
                  //  print(inttype)
                    inttype = inttype + 1
                    newQuantity = inttype
                    cell1.btnMinus.isHidden = false
                    cell1.btnPlus.isHidden = false
                }
                
                checkBool = true
            }
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
        params["device_id"] = deviceID
        params["product_id"] = newProductId
        params["quantity"] = newQuantity
     //   print(params)
        postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
         //   print(response)
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
              //  print(count1)
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
              //  print(cost)
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                cell1.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
//                cell1.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 12)
//                 cell1.btnAddtoCart.titleLabel?.font = .boldSystemFont(ofSize: 12)
                cell1.lblOrignalPrice.text = "AED \(cost)"
                cell1.btnPlus.isHidden = false
                cell1.btnMinus.isHidden = false
                cell1.btnAddtoCart.backgroundColor = .white
                cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                cell1.cartStack.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
                cell1.cartStack.layer.borderWidth = 1
                cell1.cartStack.layer.cornerRadius = 5
                cell1.cartStack.clipsToBounds =  true
               //  cell1.plusMinusStack.addBackground(color: UIColor(named: "buttonBackgroundColor")!)
                print(dict)
                //DataBaseHelper.sharedInstance.save(object: dict)
                // DataBaseHelper.sharedInstance.delete(index: coreDataindex)
                DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                // DataBaseHelper.sharedInstance.save(object: dict)
                checkBool = false
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                 NotificationCenter.default.post(name: Notification.Name("CartUpdate"), object: nil, userInfo: nil)
           //     print(DataBaseHelper.sharedInstance.getCartData())
              //  print(self.cartDatafromDb.count)
            }
            else {
                let msg = response["msg"].stringValue
                let userInfo = ["msg" : msg]
                NotificationCenter.default.post(name: Notification.Name("AddCartfailure"), object: nil, userInfo: userInfo)
            }
        }
 */
    }
    
    @objc func btnMinusAction (sender: UIButton) {
        /*
        var newProductId = String()
        var newQuantity = Int()
        var checkBool = false
        var coreDataindex = Int()
        var tempCost = String()
        cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
    //    print(DataBaseHelper.sharedInstance.getCartData())
     //   print(cartDatafromDb)
        var superview = sender.superview
        while let view = superview, !(view is UICollectionViewCell) {
            superview = view.superview
        }
        guard let cell = superview as? UICollectionViewCell else {
           // print("button is not contained in a CollectionView cell")
            return
        }
        guard let indexPath = bestSellingColView.indexPath(for: cell) else {
          //  print("failed to get index path for cell containing button")
            return
        }
        guard let cell1 = superview as? BestSellingCollectionViewCell else {
           // print("rferffddvd")
            return
        }
        // We've got the index path for the cell that contains the button, now do something with it.
        
        let cellBestSellingDict = cellBestSellingArray[indexPath.row].dictionaryValue
       // print(cellBestSellingDict)
        let productId = "\(cellBestSellingDict["stock_data"]!["product_id"].intValue)"
        for (index, element) in cartDatafromDb.enumerated() {
           // print("Item \(index): \(element)")
            
            var prouctId1 = element.product_id!
            if productId == element.product_id! {
                coreDataindex = index
                newProductId = element.product_id!
                
                let quantt = element.quantity!
                let quant1 = quantt
              //  print(quant1)
                var inttype: Int = Int(quantt)!
                print(inttype)
                print(inttype)
                inttype = inttype - 1
                newQuantity = inttype
                cell1.btnMinus.isHidden = false
                cell1.btnPlus.isHidden = false
                tempCost = element.cost
                
                //                if inttype > 0 {
                //
                //                }
                
                //                checkBool = true
            }
            else {
                cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
//                cell1.btnAddtoCart.titleLabel!.font = UIFont(name: "hind-semibold", size: 12)
//                cell1.btnAddtoCart.titleLabel!.font = .boldSystemFont(ofSize: 12)
                cell1.btnMinus.isHidden = true
                cell1.btnPlus.isHidden = true
                cell1.cartStack.layer.cornerRadius = 5
                cell1.cartStack.clipsToBounds =  true
            }
        }
        let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
        var params = [String:Any]()
        params["device_id"] = deviceID
        params["product_id"] = newProductId
        params["quantity"] = newQuantity
        print(params)
        postMethodQueryWithoutVc(apiName: "add-to-cart/", params: params) { (response : JSON) in
            print(response)
            if response["status"].intValue == 1 {
                let cartDict = response["cart_data"].dictionaryValue
                let count1 = cartDict["cartdetails"]![0]["qty"].intValue
                print(count1)
                let cost1 = cartDict["cartdetails"]![0]["new_default_price"].doubleValue
                let count = "\(count1)"
                let cost = "\(cost1)"
                print(cost)
                let dict = ["cost":cost ,"product_id":"\(newProductId)","quantity":count] as [String : Any]
                cell1.btnAddtoCart.setTitle("\(newQuantity)", for: .normal)
//                cell1.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 12)
//                cell1.btnAddtoCart.titleLabel!.font = .boldSystemFont(ofSize: 12)
                cell1.lblOrignalPrice.text = "AED \(cost)"
                cell1.btnPlus.isHidden = false
                cell1.btnMinus.isHidden = false
                cell1.btnAddtoCart.backgroundColor = .white
                cell1.btnAddtoCart.setTitleColor(.black, for: .normal)
                if count1 == 0 {
                    DataBaseHelper.sharedInstance.delete(index: coreDataindex)
                    cell1.btnAddtoCart.setTitle("ADD TO CART", for: .normal)
//                    cell1.btnAddtoCart.titleLabel?.font = UIFont(name: "hind-semibold", size: 12)
//                     cell1.btnAddtoCart.titleLabel?.font = .boldSystemFont(ofSize: 12)
                    print(cost)
                    cell1.btnPlus.isHidden = true
                    cell1.btnMinus.isHidden = true
                    cell1.lblOrignalPrice.text = "AED \(tempCost)"
                    cell1.btnAddtoCart.backgroundColor = UIColor(named: "buttonBackgroundColor")
                    cell1.btnAddtoCart.setTitleColor(.white, for: .normal)
                    cell1.cartStack.layer.cornerRadius = 5
                    cell1.cartStack.clipsToBounds =  true
                    // UIColor(named: "buttonBackgroundColor")
                }
                else {
                    DataBaseHelper.sharedInstance.editData(object: dict, i: coreDataindex)
                }
                // DataBaseHelper.sharedInstance.save(object: dict)
                print(dict)
                checkBool = false
                self.cartDatafromDb = DataBaseHelper.sharedInstance.getCartData()
                 NotificationCenter.default.post(name: Notification.Name("CartUpdate"), object: nil, userInfo: nil)
               // print(DataBaseHelper.sharedInstance.getCartData())
              //  print(self.cartDatafromDb.count)
            }
            else {
                let msg = response["msg"].stringValue
                let userInfo = ["msg" : msg]
                NotificationCenter.default.post(name: Notification.Name("AddCartfailure"), object: nil, userInfo: userInfo)
            }
      
   }
    */
    }

}
extension BestSellingTableViewCell: UICollectionViewDelegateFlowLayout{
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
         return CGSize(width: 180, height: 285)
        
    }
}
