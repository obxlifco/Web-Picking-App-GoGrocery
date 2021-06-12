//
//  BannerTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 03/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
protocol BannerSelectDelegate: class {
    func BannerTypeSelected(id: Int , slug : String , category_type : String, type : String)
}
class BannerTableViewCell: UITableViewCell ,UICollectionViewDelegate, UICollectionViewDataSource{
    @IBOutlet weak var colBanner: UICollectionView!
    
    weak var bannerdelegate : BannerSelectDelegate?
    //  @IBOutlet weak var bannerColHeight: NSLayoutConstraint!
    var cellBannerArray = [JSON]()
    override func awakeFromNib() {
        super.awakeFromNib()
    }
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // Configure the view for the selected state
    }
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return cellBannerArray.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let bannerCell = collectionView.dequeueReusableCell(withReuseIdentifier: "BannerCollectionViewCell", for: indexPath) as! BannerCollectionViewCell
        
        let bannerDict = cellBannerArray[indexPath.row].dictionaryValue
        if bannerDict["primary_image_name"]?.stringValue != nil ||  bannerDict["primary_image_name"]?.stringValue != " " {
            let brandurl = bannerDict["primary_image_name"]?.stringValue
            let fullUrl = IMAGE_URL_CATEGOERY_BANNER + brandurl!
            let url = URL(string: fullUrl)
            print(url!)
            bannerCell.imgBanner.sd_setImage(with: url!)
        }
        bannerCell.imgBanner.layer.cornerRadius = 5
         bannerCell.bannerView.addShadow1()
        return bannerCell
    }
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize{
        return  CGSize(width: colBanner.frame.width , height: 170)
    }
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        
    let bannerDict = cellBannerArray[indexPath.row].dictionaryValue
   // print(bannerDict)
         let pageTitle = bannerDict["category_name"]!.string ?? ""
        let productId = bannerDict["id"]?.int ?? 0
        let testString = bannerDict["link"]!.string ?? ""
        let splits = testString.components(separatedBy: "/")
        if splits.count != 0 {
            if splits[0] != "" {
                let slug = splits[1]
                 self.bannerdelegate?.BannerTypeSelected(id: productId, slug: "\(slug)", category_type: pageTitle, type : "121")
            }
        }
       
      //  print(splits)
      //  print(slug)
       
    }
}
extension BannerTableViewCell : UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 8.0
    }
}

