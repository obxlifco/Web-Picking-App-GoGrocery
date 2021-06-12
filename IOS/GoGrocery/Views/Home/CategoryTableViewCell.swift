//
//  CategoryTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 03/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
protocol CategorySelectDelegate: class {
    func filterTypeSelected(id: Int , slug : String , category_type : String, type : String)
}
class CategoryTableViewCell: UITableViewCell, UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
  
   @IBOutlet weak var categoryCollectionView: UICollectionView!
    @IBOutlet weak var lblShopByCategory: UILabel!
    var cellCategoryArray = [JSON]()
    var recentSelect = Bool()

    weak var delegate : CategorySelectDelegate?
    override func awakeFromNib() {
        super.awakeFromNib()
        
    }
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return self.cellCategoryArray.count
      }
    
      
      func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let catColView = collectionView.dequeueReusableCell(withReuseIdentifier: "CategoryCollectionViewCell", for: indexPath)  as! CategoryCollectionViewCell
//        catColView.addShadow2()
        let categoryDict = cellCategoryArray[indexPath.row].dictionaryValue
        print(categoryDict)
        catColView.categoryColLbl.text = categoryDict["name"]?.stringValue
//        catColView.categoryColLbl.font = .boldSystemFont(ofSize: 14)
        
     //   if categoryDict["image"]?.string!.isEmpty != true {
             let brandurl = categoryDict["image"]?.stringValue
           // print(brandurl)
            let fullUrl = IMAGE_URL_CATEGOERY + brandurl!
            let url = URL(string: fullUrl)
            catColView.categoryColImg.sd_setImage(with: url!)
      //  }
        
        
        catColView.contentView.layer.cornerRadius = 5
        catColView.layer.borderWidth = 1.0

        catColView.layer.borderColor = UIColor.clear.cgColor
        catColView.layer.masksToBounds = true

        catColView.layer.shadowColor = UIColor.gray.cgColor
        catColView.layer.shadowOffset = CGSize(width: 0, height: 2.0)
        catColView.layer.shadowRadius = 2.0
        catColView.layer.shadowOpacity = 1.0
        catColView.layer.masksToBounds = false
        catColView.layer.shadowPath = UIBezierPath(roundedRect:catColView.bounds, cornerRadius:catColView.contentView.layer.cornerRadius).cgPath
        
        catColView.categoryColView.backgroundColor = .random
        catColView.layer.cornerRadius = 5
        
        return catColView
      }
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
          let categoryDict = cellCategoryArray[indexPath.row].dictionaryValue
        let pageTitle = categoryDict["page_title"]!.stringValue
        let productId = categoryDict["id"]?.intValue
        let slug = categoryDict["slug"]!.stringValue
        let type = categoryDict["type"]!.stringValue
        self.delegate?.filterTypeSelected(id: productId!, slug: slug, category_type: "\(pageTitle)", type : type)
    }

  func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize{
    return  CGSize(width: 150, height: 135)
    }
}
