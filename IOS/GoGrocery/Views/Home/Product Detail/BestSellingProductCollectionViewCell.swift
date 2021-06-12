//
//  BestSellingProductCollectionViewCell.swift
//  GoGrocery
//
//  Created by NAV63 on 09/04/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class BestSellingProductCollectionViewCell: UICollectionViewCell {
    @IBOutlet weak var btnMinus: UIButton!
    @IBOutlet weak var btnPlus: UIButton!
    @IBOutlet weak var btnAddToCart: UIButton!
    @IBOutlet weak var cartView: UIView!
    @IBOutlet weak var lblProductName: UILabel!
    @IBOutlet weak var lblBrand: UILabel!
    @IBOutlet weak var productImage: UIImageView!
    @IBOutlet weak var btnSave: UIButton!
    @IBOutlet weak var lblProductQuantity: UILabel!
    @IBOutlet weak var lblProductPrice: UILabel!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

}
