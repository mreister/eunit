------------------------------------------------
--        ,....,
--      ,:::::::
--     ,::/^\"``.
--    ,::/, `   e`.    
--   ,::; |        '.
--   ,::|  \___,-.  c)
--   ;::|     \   '-'
--   ;::|      \
--   ;::|   _.=`\     
--   `;:|.=` _.=`\
--     '|_.=`   __\
--     `\_..==`` /
--      .'.___.-'.
--     /          \
--    ('--......--')
--    /'--......--'\
--    `"--......--"`
--
-- Created By: 
--
------------------------------------------------



library ieee ;
use ieee.std_logic_1164.all ;
use ieee.numeric_std.all ;

entity many_ports is
  port (
  -- inputs
  	data_i : in wavel_t;
	clk_i         : in std_logic;
	rst_i         : in std_logic;

	-- outputs

  data_o        : out std_logic_vector(7 downto 0);
  data_valid_o  : out std_logic

  ) ;
end entity ; -- many_ports

architecture arch of many_ports is

begin


identifier_inst : entity work.many_ports
port map (
    data_i 	=> data_i -- wavel_t,
    clk_i 	=> clk_i -- std_logic,
    rst_i 	=> rst_i -- std_logic,
    data_o 	=> data_o -- std_logic_vector(7 downto 0
);

end architecture ; -- arch