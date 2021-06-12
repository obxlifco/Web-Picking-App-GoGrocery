//
//  DealsOfTheDayTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 03/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class DealsOfTheDayTableViewCell: UITableViewCell ,UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
    
    
    @IBOutlet weak var dealsCollectionView: UICollectionView!
      @IBOutlet weak var lblDealsOfTheDay: UILabel!
    @IBOutlet weak var lblShowAll: UILabel!
    var cellDealsArray = [JSON]()
    override func awakeFromNib() {
        super.awakeFromNib()
        
    }
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // Configure the view for the selected state
    }
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
       // return cellDealsArray.count
        return 0
    }
    //150 210
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "DealsOfTheDayCollectionViewCell", for: indexPath) as! DealsOfTheDayCollectionViewCell
  /*
        let dealsOfTheDayDict = cellDealsArray[indexPath.row].dictionaryValue
      //  print(dealsOfTheDayDict)
        if dealsOfTheDayDict["product_image"]?.arrayValue.count != 0 {
            let productImagesArray = dealsOfTheDayDict["product_image"]?.arrayValue
            
            let imageDict = productImagesArray![0].dictionaryValue
            //        let imageUrl = imageDict["img"]?.stringValue
            
            if let brandurl = imageDict["image"]?.stringValue{
                //   let brandurl = imageDict["image"]?.stringValue
                let fullUrl = IMAGE_URL_CATEGOERY + brandurl
                let url = URL(string: fullUrl)
              //  print(url!)
                cell.imgDeals.sd_setImage(with: url!)
            }
            if let foodType = dealsOfTheDayDict["veg_nonveg_type"]?.stringValue {
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
            if dealsOfTheDayDict["name"]?.stringValue != nil{
                cell.lblTitle.text = "\(dealsOfTheDayDict["name"]?.stringValue ?? " ")"
                
            }
            else {
                cell.lblTitle.isHidden = true
            }
            let channnelPrice = dealsOfTheDayDict["channel_price"]!.intValue
            let newDefaultPrice = dealsOfTheDayDict["new_default_price"]!.intValue
            let newDefaultPriceUnit = dealsOfTheDayDict["new_default_price_unit"]!.intValue
            let discountPrice = dealsOfTheDayDict["discount_price"]!.intValue
            let discountAmount = dealsOfTheDayDict["discount_amount"]!.intValue
            
            if channnelPrice < newDefaultPriceUnit {
                cell.lblOrignalPrice.text = "$ \(channnelPrice)"
                cell.lblDiscountedPrice.isHighlighted = true
                cell.lblDiscount.isHidden = true
            }
            else {
                cell.lblOrignalPrice.text = "$ \(newDefaultPriceUnit)"
                cell.lblDiscountedPrice.text = "$ \(channnelPrice)"
                cell.lblDiscount.text = "\(discountAmount)% off"
            }
            
        }
        cell.btnSave.tag = indexPath.row
        cell.btnSave.addTarget(self, action: #selector(btnSaveAction), for: .touchUpOutside)
        cell.btnPlus.tag = indexPath.row
        cell.btnPlus.addTarget(self, action: #selector(btnPlusAction), for: .touchUpInside)
        cell.btnMinus.tag = indexPath.row
        cell.btnMinus.addTarget(self, action: #selector(btnMinusAction), for: .touchUpInside)
        cell.btnText.tag = indexPath.row
        cell.btnText.addTarget(self, action: #selector(btnTextAction), for: .touchUpInside)
        cell.btnText.setTitle("0", for: .normal)
        
        cell.plusMinusStack.layer.borderColor = UIColor.green.cgColor
        cell.plusMinusStack.layer.borderWidth = 1
        cell.layer.borderColor = UIColor.darkGray.cgColor
        cell.layer.borderWidth = 1
         cell.addShadow2()
        */
        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize{
        return  CGSize(width: 200, height: 440)
    }
    
    //    MARK:- Button Actions
    @objc func btnSaveAction(sender: UIButton) {
        
    }
    @objc func btnPlusAction(sender: UIButton) {
        
    }
    
    @objc func btnMinusAction(sender: UIButton) {
        
    }
    
    @objc func btnTextAction(sender: UIButton) {
        
    }
    
    
}
