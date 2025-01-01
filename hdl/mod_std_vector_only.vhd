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

entity hello is
generic(
	DATA_SIZE_I : in natural
);
  port (
  -- inputs
	clk_i         : in std_logic;
	rst_i         : in std_logic;

	-- outputs
  data_o        : out std_logic_vector(7 downto 0);
  data_valid_o  : out std_logic

  ) ;
end entity ; -- 

architecture arch of  hello is

begin


constant identifier_COUNTER_SIZE : integer := 8;
signal identifier_sig :  unsigned((identifier_COUNTER_SIZE - 1) downto 0);
signal identifier_en_sig : std_logic;

-----------------------------------------
-- identifier
-----------------------------------------
identifier_inst : entity work.clear_counter 
generic map(
	COUNTER_SIZE => identifier_COUNTER_SIZE
)
port map (
	clk_in => clk_i,
	rst_in => rst_i,
	counter_en_in => identifier_en_sig,
	--
	counter_o => identifier_sig
) ;

counter_inst : entity work.counter
generic map (
    BUS_WIDTH => BUS_WIDTH
)
port map (
    clock => clock -- logic,
    reset => reset -- logic,
    logic => logic -- logic
);
end architecture ; -- arch