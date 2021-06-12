//
//  SimilarProductTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 17/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
class SimilarProductTableViewCell: UITableViewCell ,UICollectionViewDelegate, UICollectionViewDataSource {
    @IBOutlet weak var similarProductCollectionView: UICollectionView!
    var screenSize: CGRect!
    var screenWidth: CGFloat!
    var screenHeight: CGFloat!
       private let spacing:CGFloat = 16
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
       
        similarProductCollectionView.addShadow1()
        similarProductCollectionView.delegate = self
        similarProductCollectionView.dataSource = self
    }
    func reloadCollectionView() -> Void {
        self.similarProductCollectionView.delegate = self
        self.similarProductCollectionView.dataSource = self
        self.similarProductCollectionView.reloadData()
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
           return 10
       }
    
       func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
           let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "SimilarProductCollectionViewCell", for: indexPath) as! SimilarProductCollectionViewCell
           return cell
       }
    
//    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
//        let productDict = productArray[indexPath.row].dictionaryValue
//        let sourceDict = productDict["_source"]!.dictionaryValue
//        print("tapped")
//        print(sourceDict)
//        let slug = sourceDict["slug"]!.stringValue
//        //  print(slug)
//        // print(productDict)
//        let productId = productDict["_id"]!.intValue
//        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
//        vc.slugInDetail = slug
//        vc.prId = productId
//        self.navigationController?.pushViewController(vc, animated: true)
//    }
}

extension SimilarProductTableViewCell: UICollectionViewDelegateFlowLayout{
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 2
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let numberOfItemsPerRow:CGFloat = 2
        let spacingBetweenCells:CGFloat = 16
        
        let totalSpacing = (2 * self.spacing) + ((numberOfItemsPerRow - 1) * spacingBetweenCells) //Amount of total spacing in a row
        
        if let collection = self.similarProductCollectionView {
            let width = (collection.bounds.width - totalSpacing)/numberOfItemsPerRow
            return CGSize(width: 220, height: 340)
        }
        else{
            return CGSize(width: 0, height: 0)
        }
    }
}
