import matplotlib.pyplot as plt
import matplotlib        as plt

def plot1(country1, country2):
    
    """
    NEEDS REWORK!!!
    [list(DF1.iloc[:, 0]), DF1, name1, alpha1, color1]
    [list(DF2.iloc[:, 0]), DF2, name2, alpha2, color2]
    """
    fig, axs = plt.subplots(2, sharex = True, gridspec_kw = {"hspace": 0})
    plt.suptitle(country1[3] + " vs. " + country2[3], fontsize = "30")
    axs[0].set_title(country1[2], fontsize = 20, y = 0.8)
    axs[1].set_title(country2[2], fontsize = 20, y = 0)
    axs[1].set_xlabel("Year")
    axs[0].set_ylabel(country1[0])
    axs[1].set_ylabel(country2[0])
    ylim_lower = min(min([x for x in country1[0] if str(x) != 'nan']), min([x for x in country2[0] if str(x) != 'nan']))
    ylim_upper = max(max([x for x in country1[0] if str(x) != 'nan']), max([x for x in country2[0] if str(x) != 'nan']))
    axs[0].set_ylim(ylim_lower, ylim_upper)
    axs[1].set_ylim(ylim_lower, ylim_upper)
    axs[0].plot(country1[1].iloc[:, 0], c = country1[4])
    axs[1].plot(country2[1].iloc[:, 0], c = country2[4])
    return fig

def plot2(country1, country2, index_full):
    """
    NEEDS REWORK!!!
    """
    fig = plt.figure()
    plt.plot(country1[0][country1[1]], label = country1[2], c = country1[3])
    plt.plot(country2[0][country2[1]], label = country2[2], c = country2[3])
    plt.xlabel("Time Index")
    plt.ylabel(index_full)
    plt.legend()
    return fig

def plot3(country1_motif_index, country1_mp):
    """
    NEEDS REWORK!!!
    """
    fig = plt.figure()
    plt.xlabel('Subsequence')
    plt.ylabel('Matrix Profile')
    plt.scatter(country1_motif_index, country1_mp[country1_motif_index, 0], c = 'red', s = 100)
    plt.plot(country1_mp[:,0])
    return fig

def text1(country1_mp, country1_motif_index):
    """
    NEEDS REWORK!!!
    """
    print("Matrix profile length: ",       len(country1_mp[:, 0]))
    print("Lowest value found at index: ", country1_motif_index)
    print("Matrix Profile: ")
    print(country1_mp[:, 0])

def text2(country1_mp, name1, name2):
    """
    NEEDS REWORK!!!
    """
    country1_motif_index = country1_mp[:, 0].argmin()
    print(f'The motif is located at index {country1_motif_index} of "' + name1 + ' Matrix Profile"')
    print("In fact, the index location of its nearest neighbor in country2 is stored in") 
    country2_motif_index = country1_mp[country1_motif_index, 1]
    print(f'The motif that is located at index {country2_motif_index} of "' + name2 + ' Matrix Profile"')

def plot4(country1, country2, index_full):
    """
    NEEDS REWORK!!!
    """
    fig4 = plt.figure()
    plt.plot(country1[0], label = country1[1], c = country1[2])
    plt.plot(country2[0], label = country2[1], c = country2[2])
    plt.xlabel('Time Index')
    plt.ylabel(index_full)
    plt.legend()

def plot5(country1, country2, index_full):
    """
    NEEDS REWORK!!!
    """
    fig5 = plt.figure()
    plt.plot(country1[0][country1[1]], label = country1[2], c = country1[3])
    plt.plot(country2[0][country2[1]], label = country2[2], c = country2[3])
    plt.xlabel('Time Index')
    plt.ylabel(index_full)
    plt.legend()