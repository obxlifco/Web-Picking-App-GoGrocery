//
//  PresentOrderTableViewCell.swift
//  GoGrocery
//
//  Created by Nav121 on 05/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class PresentOrderTableViewCell: UITableViewCell {
    
    
    @IBOutlet weak var containerView: UIView!
    @IBOutlet weak var orderNoLabel: UILabel!
    @IBOutlet weak var orederDateLabel: UILabel!
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var paymentStatusLabel: UILabel!
    @IBOutlet weak var orderStatusLabel: UILabel!
      @IBOutlet weak var paymentModeLabel: UILabel!
    
    
    
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
