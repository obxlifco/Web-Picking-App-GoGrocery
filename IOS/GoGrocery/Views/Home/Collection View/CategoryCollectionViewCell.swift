//
//  CategoryCollectionViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 03/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class CategoryCollectionViewCell: UICollectionViewCell {
    @IBOutlet weak var categoryColView: UIView!
    @IBOutlet weak var categoryColLbl: UILabel!
    @IBOutlet weak var categoryColImg: UIImageView!
    
    
    override var bounds: CGRect {
        didSet {
            self.layoutIfNeeded()
        }
    }
    override func layoutSubviews() {
        super.layoutSubviews()
        
//        self.setCircularImageView()
    }
    
//    func setCircularImageView() {
////        categoryColView.backgroundColor = .orange
//        let rectShape = CAShapeLayer()
//        rectShape.bounds = categoryColView.frame
//        rectShape.position = categoryColView.center
//        rectShape.path = UIBezierPath(roundedRect: categoryColView.bounds, byRoundingCorners: [.topRight  , .topLeft], cornerRadii: CGSize(width: 5, height: 5)).cgPath
//        categoryColView.layer.mask = rectShape
////        categoryColView.invalidateIntrinsicContentSize()
//        categoryColView.backgroundColor = .random
//    }
        func setCircularImageView() {
    //        categoryColView.backgroundColor = .orange
            let rectShape = CAShapeLayer()
            rectShape.bounds = categoryColView.frame
            rectShape.position = categoryColView.center
            rectShape.path = UIBezierPath(roundedRect: categoryColView.bounds, byRoundingCorners: [.topRight  , .topLeft], cornerRadii: CGSize(width: 5, height: 5)).cgPath
            categoryColView.layer.mask = rectShape
    //        categoryColView.invalidateIntrinsicContentSize()
            categoryColView.backgroundColor = .random
        }
}
