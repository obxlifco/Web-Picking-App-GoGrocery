//
//  SearchDisplayTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 05/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class SearchDisplayTableViewCell: UITableViewCell {

    @IBOutlet weak var imgImage: UIImageView!
    @IBOutlet weak var lblTitle: UILabel!
    @IBOutlet weak var lblQuantity: UILabel!
    @IBOutlet weak var lblPrice: UILabel!

    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
