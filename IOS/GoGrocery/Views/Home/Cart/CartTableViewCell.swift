//
//  CartTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 21/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class CartTableViewCell: UITableViewCell {

     @IBOutlet weak var imgProduct: UIImageView!
     @IBOutlet weak var lblTitle: UILabel!
     @IBOutlet weak var lblOrignalPrice: UILabel!
    @IBOutlet weak var btnAddtoCart: UIButton!
     @IBOutlet weak var plusMinusStack: UIStackView!
    @IBOutlet weak var btnPlus: UIButton!
    @IBOutlet weak var btnMinus: UIButton!
      @IBOutlet weak var cartStack: UIView!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    

}
