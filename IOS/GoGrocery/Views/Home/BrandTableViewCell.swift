//
//  BrandTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 03/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
protocol BrandSelectDelegate: class {
    func BrandTypeSelected(id: Int , slug : String , category_type : String, type : String, brandSelect : Bool)
}
class BrandTableViewCell: UITableViewCell ,UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
 @IBOutlet weak var brandCollectionView: UICollectionView!
    @IBOutlet weak var lblShopByBrand: UILabel!
    var cellBrandCell = [JSON]()
     var cellBrandTemp = [JSON]()
    weak var branddelegate : BrandSelectDelegate?
    override func awakeFromNib() {
        super.awakeFromNib()
      //  print(cellBrandCell)
      
          lblShopByBrand.font = .boldSystemFont(ofSize: 16)
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
   // shouldInvalidateLayoutForBoundsChange
    
  
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        1
    }
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
     //   print(self.cellBrandCell.count)
        for index in self.cellBrandCell {
           // print(index)
            if let tempL = index["brand_logo"].string {
             self.cellBrandTemp.append(index)
            }
        }
        self.cellBrandCell.removeAll()
        self.cellBrandCell = self.cellBrandTemp
        return cellBrandCell.count
      }
      
      func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let brandCell = collectionView.dequeueReusableCell(withReuseIdentifier: "ShopBrandCollectionViewCell", for: indexPath) as! ShopBrandCollectionViewCell
     //   DispatchQueue.global().async {
            let brandDict = self.cellBrandCell[indexPath.row].dictionaryValue
            if let brandurl =  brandDict["brand_logo"]?.string {
//                 let brandurl = brandDict["brand_logo"]?.stringValue
                let fullUrl = IMAGE_URL_BRAND + brandurl
                let url = URL(string: fullUrl)
           //     print(url!)
                brandCell.imgBrands.sd_setImage(with: url!)
//                brandCell.addShadow2()
           // }
        }
        brandCell.imgBrands.layer.cornerRadius = 5
        brandCell.brandView.addShadow1()
         brandCell.brandView.layer.cornerRadius = 5
        return brandCell
      }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize{
      return  CGSize(width: 200, height: 125)
      }
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
              let brandDict = self.cellBrandCell[indexPath.row].dictionaryValue
              //  print(brandDict)
         let pageTitle = brandDict["name"]!.stringValue
        let productId = brandDict["id"]?.intValue
        let slug = brandDict["slug"]?.stringValue
        self.branddelegate?.BrandTypeSelected(id: productId!, slug: "\(slug!)", category_type: pageTitle, type : "121", brandSelect: true)
    }
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
         return 0
     }
    
}
