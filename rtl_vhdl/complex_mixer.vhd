library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity complex_mixer is
    port (
        clk        : in  std_logic;
        rst        : in  std_logic;
        -- 16-bit signed input data stream channel
        din_real   : in  std_logic_vector(15 downto 0);

        -- Local oscillator 16-bit coefficient input
        nco_cos    : in  std_logic_vector(15 downto 0);

        -- Registered 32-bit product output
        dout_mixed : out std_logic_vector(31 downto 0)
    );
end entity complex_mixer;

architecture rtl of complex_mixer is
    signal r_prod_32bit : signed(31 downto 0);
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                r_prod_32bit <= (others => '0');
            else
                r_prod_32bit <= signed(din_real) * signed(nco_cos);
            end if;
        end if;
    end process;

    dout_mixed <= std_logic_vector(r_prod_32bit);
end architecture rtl;