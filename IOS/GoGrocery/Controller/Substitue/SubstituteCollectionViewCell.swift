//
//  SubstituteCollectionViewCell.swift
//  GoGrocery
//
//  Created by NAV63 on 26/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class SubstituteCollectionViewCell: UICollectionViewCell {
    @IBOutlet weak var imgSubsImg: UIImageView!
    @IBOutlet weak var lblSubProductName: UILabel!
    @IBOutlet weak var lblSubProductPrice: UILabel!
    @IBOutlet weak var lblSubProductWeight: UILabel!
    @IBOutlet weak var btnAddtoCart: UIButton!
     @IBOutlet weak var plusMinusStack: UIStackView!
    @IBOutlet weak var btnPlus: UIButton!
    @IBOutlet weak var btnMinus: UIButton!
     @IBOutlet weak var cartStack: UIView!
      @IBOutlet weak var lblSKUName: UILabel!
}
