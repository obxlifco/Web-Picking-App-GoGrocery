//
//  BestSellingCollectionViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 06/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class BestSellingCollectionViewCell: UICollectionViewCell {
     @IBOutlet weak var btnSave: UIButton!
     @IBOutlet weak var btnVeg: UIButton!
     @IBOutlet weak var imgDeals: UIImageView!
     @IBOutlet weak var lblSubtitle: UILabel!
     @IBOutlet weak var lblTitle: UILabel!
     @IBOutlet weak var lblOrignalPrice: UILabel!
    @IBOutlet weak var btnAddtoCart: UIButton!
     @IBOutlet weak var plusMinusStack: UIStackView!
    @IBOutlet weak var btnPlus: UIButton!
    @IBOutlet weak var btnMinus: UIButton!
     @IBOutlet weak var cartStack: UIView!
      @IBOutlet weak var lblProductWeight: UILabel!
    
        override var bounds: CGRect {
            didSet {
                self.layoutIfNeeded()
            }
        }
        override func layoutSubviews() {
            super.layoutSubviews()
            
            self.setCircularImageView()
        }
        
        func setCircularImageView() {
            cartStack.layer.cornerRadius = 5
            cartStack.clipsToBounds =  true
        }
}
