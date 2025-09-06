nirmal : dialog {
          label = "DESIGN OF STAIRCASE  (By Nirmal Suthar)";
          :text {
          label = "This program is supported by (Mr. chaturbhuj suthar)";
          }
          : column {
            : boxed_column {
            label = "GIVE FOLLOWING DATA FOR DESIGN";
              : edit_box {
                key = "clength";
                label = "CLEAR SPAN OF STAIRCASE IN MM";
                edit_width = 5;
                value = "";
                
              }
              : edit_box {
                key = "wstair";
                label = "width of staircase IN MM";
                edit_width = 5;
                value = "";
                
              }
              : edit_box {
                key = "bwid";
                label = "Breadth of wall or beam IN MM";
                edit_width = 5;
                value = "";
                
              }
              : edit_box {
                key = "lload";
                label = "LIVE LOAD IN KN/SQM";
                edit_width = 5;
                value = "";
              }
              :edit_box {
               key = "ffload";
               label = "FLOOR FINISH LOAD IN KN/SQM";
               edit_width = 5;
               value = "";
              }
              :edit_box {
               key = "nriser";
               label = "no. of riser";
               edit_width = 5;
               value = "";
              }
              :edit_box {
               key = "riser";
               label = "RISER IN MM";
               edit_width = 5;
               value = "";
               }
              :edit_box {
               key = "tread";
               label = "TREAD IN MM";
               edit_width = 5;
               value = "";
              }
              :edit_box {
               key = "cgrade";
               label = "GRADE OF CONCRETE (M20)";
               edit_width = 5;
               value = "";
               }
               :edit_box {
               key = "sgrade";
               label = "GRADE OF STEEL (Fe415) ";
               edit_width = 5;
               value = "";
               }
               : image {
  		key = "staircase";
  		height = 15;
  		width = 15; 
     		color = 280;
  		is_enabled = false;
  		is_tab_stop = false;
		}
		:column {
               
                label = "CONTACT INFORMATION : (Mobile no. 09352508947)";
                
                
             }
            }
            : boxed_row {
              : button {
                key = "accept";
                label = " DESIGN AND SECTIONAL DRAWING ";
                is_default = true;
              }
              : button {
                key = "cancel";
                label = " Cancel ";
                is_default = false;
                is_cancel = true;
              }
            }
          }

}

