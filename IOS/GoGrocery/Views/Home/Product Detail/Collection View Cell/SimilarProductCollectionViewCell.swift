//
//  SimilarProductCollectionViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 17/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class SimilarProductCollectionViewCell: UICollectionViewCell {
    @IBOutlet weak var btnSave: UIButton!
     @IBOutlet weak var imgImage: UIImageView!
     @IBOutlet weak var lblTitle: UILabel!
     @IBOutlet weak var lblOrignalPrice: UILabel!
    @IBOutlet weak var btnAddtoCart: UIButton!
     @IBOutlet weak var plusMinusStack: UIStackView!
    @IBOutlet weak var btnPlus: UIButton!
    @IBOutlet weak var btnMinus: UIButton!
      @IBOutlet weak var productListView: UIView!
    
    @IBOutlet weak var lblProductWeight: UILabel!
    
    @IBOutlet weak var cartStack: UIView!
    
    
}

