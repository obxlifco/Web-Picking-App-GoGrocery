//
//  ProductListingCollectionViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 11/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class ProductListingCollectionViewCell: UICollectionViewCell {
     @IBOutlet weak var btnSave: UIButton!
     @IBOutlet weak var imgImage: UIImageView!
     @IBOutlet weak var lblBrand: UILabel!
     @IBOutlet weak var lblTitle: UILabel!
     @IBOutlet weak var lblOrignalPrice: UILabel!
    @IBOutlet weak var btnAddtoCart: UIButton!
     @IBOutlet weak var plusMinusStack: UIStackView!
    @IBOutlet weak var btnPlus: UIButton!
    @IBOutlet weak var btnMinus: UIButton!
      @IBOutlet weak var productListView: UIView!
    @IBOutlet weak var lblTitleHeightConstant: NSLayoutConstraint!
    @IBOutlet weak var lblPriceheightConstant: NSLayoutConstraint!
    @IBOutlet weak var cartStack: UIView!
      @IBOutlet weak var lblProductWeight: UILabel!
     @IBOutlet weak var lblDiscount: UILabel!
    @IBOutlet weak var lblStrikedPrice: UILabel!
}
